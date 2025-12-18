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

@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return app.send_static_file("sitemap.xml")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        input_movie = request.form["movie"].strip()
        if not input_movie:
            return render_template("error.html", movie="")
        
        recommendations = recommend_movies(input_movie, data, model, movie_encoder, genre_encoder, director_encoder)
        
        if recommendations:
            return render_template("recommendations.html", input_movie=input_movie, recommendations=recommendations)
        else:
            return render_template("error.html", movie=input_movie)
    except Exception as e:
        print(f"Error in recommend: {str(e)}")
        return render_template("error.html", movie=input_movie if 'input_movie' in locals() else "")

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
    input_movie_data = data[data['movie_encoded'] == input_movie_encoded].iloc[0]
    input_movie_genres = set(input_movie_data['genres_list'])
    input_movie_year = input_movie_data['year']
    input_movie_director = input_movie_data['director']
    
    # Filter out the input movie first to reduce computation
    other_movies = data[data['movie'] != input_movie].copy()
    
    # Optimized genre overlap calculation
    input_genres_set = input_movie_genres
    input_genres_len = len(input_genres_set) if len(input_genres_set) > 0 else 1
    
    def calc_overlap(genres):
        if isinstance(genres, list) and len(genres) > 0:
            return len(set(genres).intersection(input_genres_set)) / input_genres_len
        return 0.0
    
    # Use list comprehension (faster than apply for simple operations)
    other_movies['genre_overlap'] = [calc_overlap(g) for g in other_movies['genres_list']]
    
    # Filter by minimum genre overlap first (reduces dataset size)
    filtered_movies = other_movies[other_movies['genre_overlap'] >= min_genre_overlap].copy()
    
    # Add director match flag
    filtered_movies['director_match'] = (filtered_movies['director'] == input_movie_director)
    
    # Prioritize: same year, same director, high rating
    filtered_movies['same_year'] = (filtered_movies['year'] == input_movie_year)
    
    # Create a composite score for sorting
    filtered_movies['score'] = (
        filtered_movies['genre_overlap'] * 0.4 +  # Genre match weight
        filtered_movies['same_year'].astype(int) * 0.3 +  # Same year bonus
        filtered_movies['director_match'].astype(int) * 0.2 +  # Same director bonus
        (filtered_movies['rating'] / 10.0) * 0.1  # Rating weight
    )
    
    # Sort by composite score and rating
    filtered_movies = filtered_movies.sort_values(
        by=['score', 'rating', 'genre_overlap'], 
        ascending=[False, False, False]
    )
    
    # Get top recommendations
    top_recommendations = filtered_movies.head(num_recommendations * 2)  # Get more, then filter
    
    # Build detailed recommendations
    detailed_recommendations = []
    for idx, row in top_recommendations.iterrows():
        reason_parts = [f"Recommended because it shares {int(row['genre_overlap'] * 100)}% genre match with '{input_movie}'."]
        
        if row['same_year']:
            reason_parts.append(f" It was released in the same year ({input_movie_year}).")
        if row['rating'] >= high_rating_threshold:
            reason_parts.append(f" Also, it has a high rating of {row['rating']:.1f}.")
        if row['director_match']:
            reason_parts.append(f" Moreover, it was directed by the same director ({input_movie_director}).")
        
        detailed_recommendations.append({
            'movie': row['movie'],
            'rating': float(row['rating']),
            'year': int(row['year']),
            'genres': row['genres'],
            'genre_overlap': float(row['genre_overlap']),
            'overview': row['overview'],
            'revenue': format_revenue(row['revenue']),
            'reason_for_recommendation': ' '.join(reason_parts)
        })
        
        # Stop when we have enough recommendations
        if len(detailed_recommendations) >= num_recommendations:
            break
    
    return detailed_recommendations

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
