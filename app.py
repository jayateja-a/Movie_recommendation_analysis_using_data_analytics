from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Embedding, Flatten, Dense, Input, Concatenate
from tensorflow.keras.optimizers import Adam

# Initialize Flask app
app = Flask(__name__)

# File paths for saved models and encoders
MODEL_PATH = 'movie_recommendation_model.h5'
ENCODERS_PATH = 'encoders.pkl'
DATA_PATH = 'final_final_dataset.csv'

def load_or_train_model():
    """Load saved model and encoders if they exist, otherwise train and save them"""
    
    # Check if model and encoders exist
    if os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH):
        print("Loading saved model and encoders...")
        model = load_model(MODEL_PATH)
        with open(ENCODERS_PATH, 'rb') as f:
            encoders = pickle.load(f)
        movie_encoder = encoders['movie_encoder']
        genre_encoder = encoders['genre_encoder']
        director_encoder = encoders['director_encoder']
        
        # Load and preprocess data
        data = pd.read_csv(DATA_PATH)
        data = data[['index', 'director', 'duration', 'genres', 'movie', 'language', 'country', 'year', 'rating', 'overview', 'revenue']]
        data = data.dropna()
        data['genres_list'] = data['genres'].str.split('|')
        data['year'] = data['year'].astype(int)
        data['movie_encoded'] = movie_encoder.transform(data['movie'])
        data['genre_encoded'] = genre_encoder.transform(data['genres'])
        data['director_encoded'] = director_encoder.transform(data['director'])
        
        print("Model and encoders loaded successfully!")
        return model, data, movie_encoder, genre_encoder, director_encoder
    
    else:
        print("Training new model...")
        # Load your dataset (ensure overview and revenue columns are included)
        data = pd.read_csv(DATA_PATH)
        
        # Preprocess the data
        data = data[['index', 'director', 'duration', 'genres', 'movie', 'language', 'country', 'year', 'rating', 'overview', 'revenue']]
        data = data.dropna()  # Drop rows with missing values
        
        # Encode categorical columns (movies, genres, director, etc.)
        movie_encoder = LabelEncoder()
        data['movie_encoded'] = movie_encoder.fit_transform(data['movie'])
        
        genre_encoder = LabelEncoder()
        data['genre_encoded'] = genre_encoder.fit_transform(data['genres'])
        
        director_encoder = LabelEncoder()
        data['director_encoded'] = director_encoder.fit_transform(data['director'])
        
        # Split the genres into lists of individual genres
        data['genres_list'] = data['genres'].str.split('|')
        
        # Convert year to integer to avoid decimal values
        data['year'] = data['year'].astype(int)
        
        # Prepare input data for the model
        num_movies = len(movie_encoder.classes_)
        num_genres = len(genre_encoder.classes_)
        
        # Model Definition (Matrix Factorization)
        movie_input = Input(shape=(1,))
        genre_input = Input(shape=(1,))
        
        movie_embedding = Embedding(num_movies, 50)(movie_input)
        genre_embedding = Embedding(num_genres, 10)(genre_input)
        
        movie_flat = Flatten()(movie_embedding)
        genre_flat = Flatten()(genre_embedding)
        
        # Concatenate the embeddings
        concat = Concatenate(axis=-1)([movie_flat, genre_flat])
        
        # Dense layers for final prediction
        dense = Dense(64, activation='relu')(concat)
        output = Dense(1, activation='linear')(dense)
        
        # Build and compile the model
        model = Model(inputs=[movie_input, genre_input], outputs=output)
        model.compile(optimizer=Adam(), loss='mean_squared_error')
        
        # Prepare training data
        X_train = [data['movie_encoded'].values, data['genre_encoded'].values]
        y_train = data['rating'].values
        
        # Train the model
        print("Training model (this may take a few minutes)...")
        model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1)
        
        # Save model and encoders
        model.save(MODEL_PATH)
        with open(ENCODERS_PATH, 'wb') as f:
            pickle.dump({
                'movie_encoder': movie_encoder,
                'genre_encoder': genre_encoder,
                'director_encoder': director_encoder
            }, f)
        
        print("Model and encoders saved successfully!")
        return model, data, movie_encoder, genre_encoder, director_encoder

# Load or train model on startup
model, data, movie_encoder, genre_encoder, director_encoder = load_or_train_model()

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    input_movie = request.form["movie"]
    recommendations = recommend_movies(input_movie, data, model, movie_encoder, genre_encoder, director_encoder)
    
    if recommendations:
        return render_template("recommendations.html", input_movie=input_movie, recommendations=recommendations)
    else:
        return render_template("error.html", movie=input_movie)

def format_revenue(value):
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.2f}K"
    else:
        return f"${value:.2f}"

def recommend_movies(input_movie, data, model, movie_encoder, genre_encoder, director_encoder,
                     num_recommendations=10, min_genre_overlap=0.5, high_rating_threshold=7.0):
    if input_movie not in movie_encoder.classes_:
        return []
    
    # Encode the input movie and extract its attributes
    input_movie_encoded = movie_encoder.transform([input_movie])[0]
    input_movie_genres = data[data['movie_encoded'] == input_movie_encoded]['genres_list'].values[0]
    input_movie_year = data[data['movie_encoded'] == input_movie_encoded]['year'].values[0]
    input_movie_director = data[data['movie_encoded'] == input_movie_encoded]['director'].values[0]
    
    all_movies = data.copy()
    movie_indices = all_movies['movie_encoded'].values
    genre_indices = all_movies['genre_encoded'].values
    predictions = model.predict([movie_indices, genre_indices])
    
    recommended_movies = pd.DataFrame({
        'movie': all_movies['movie'].values,
        'director': all_movies['director'].values,
        'rating': all_movies['rating'].values,
        'year': all_movies['year'].values,
        'genres': all_movies['genres'].values,
        'genres_list': all_movies['genres_list'].values,
        'overview': all_movies['overview'].values,
        'revenue': all_movies['revenue'].values
    })
    
    def calculate_genre_overlap(movie_genres):
        common_genres = set(input_movie_genres).intersection(set(movie_genres))
        return len(common_genres) / len(set(input_movie_genres))
    
    recommended_movies['genre_overlap'] = recommended_movies['genres_list'].apply(calculate_genre_overlap)
    recommended_movies['director_match'] = recommended_movies['director'].apply(lambda x: x == input_movie_director)
    
    same_year_movies = recommended_movies[recommended_movies['year'] == input_movie_year]
    same_year_movies = same_year_movies[same_year_movies['genre_overlap'] >= min_genre_overlap]
    same_year_movies = same_year_movies.sort_values(by=['genre_overlap', 'rating'], ascending=[False, False])
    
    director_match_movies = recommended_movies[recommended_movies['director_match']]
    
    # Combine same year movies and at least one movie with the same director
    combined_recommendations = pd.concat([same_year_movies, director_match_movies]).drop_duplicates(subset='movie')
    
    # Exclude the input movie
    combined_recommendations = combined_recommendations[combined_recommendations['movie'] != input_movie]
    combined_recommendations = combined_recommendations.sort_values(by=['genre_overlap', 'rating'], ascending=[False, False])
    
    # Limit the number of recommendations
    combined_recommendations = combined_recommendations.head(num_recommendations)
    
    detailed_recommendations = []
    for i, row in combined_recommendations.iterrows():
        reason = f"Recommended because it shares {int(row['genre_overlap'] * 100)}% genre match with '{input_movie}'."
        if row['year'] == input_movie_year:
            reason += f" It was released in the same year ({input_movie_year})."
        if row['rating'] >= high_rating_threshold:
            reason += f" Also, it has a high rating of {row['rating']}."
        if row['director'] == input_movie_director:
            reason += f" Moreover, it was directed by the same director ({input_movie_director})."
        
        detailed_recommendations.append({
            'movie': row['movie'],
            'rating': row['rating'],
            'year': row['year'],
            'genres': row['genres'],
            'genre_overlap': row['genre_overlap'],
            'overview': row['overview'],
            'revenue': format_revenue(row['revenue']),
            'reason_for_recommendation': reason
        })
    
    return detailed_recommendations

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
