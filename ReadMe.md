README:
Movie Recommendation System and Analysis
Table of Contents
1.	Introduction
2.	Features
3.	Technologies Used
4.	Setup and Installation
5.	Dataset
6.	Model Overview
7.	Application Workflow
8.	File Descriptions
9.	Usage
10.	Screenshots
11.	Future Enhancements
Introduction
This project is a Movie Recommendation System that provides movie recommendations based on user input. It uses a deep learning model for recommendations, along with data visualizations to analyze movie trends and industry patterns.
Features
•	Predicts movies based on genre, year, director, and ratings.
•	Provides reasons for each recommendation (e.g., genre overlap, same director, etc.).
•	Displays analysis on top genres, directors, and revenue trends.
•	Interactive web interface built with Flask.
Technologies Used
•	Programming Language: Python
•	Web Framework: Flask
•	Deep Learning Framework: TensorFlow/Keras
•	Data Analysis and Visualization: Pandas, Matplotlib, Seaborn
•	Frontend: HTML, CSS
•	Data Preprocessing: Scikit-learn
Setup and Installation
Prerequisites
•	Python 3.7 or above
•	Libraries: TensorFlow, Flask, Pandas, Scikit-learn, Matplotlib, Seaborn

Steps
1.	Download all the files for this project into a single folder on your computer
2.	Open the visual studio code with the folder contents in separate workspace
3.	cd <foldername> in terminal
4.	Install dependencies: 
   ```bash
   pip install -r requirements.txt
   ```
5.	Place the dataset file (final_final_dataset.csv) in the project directory.
6.	Run the Flask app: 
   ```bash
   python app.py
   ```
7.	Open your browser and navigate to http://127.0.0.1:5000/.

**Note:** On first run, the model will be trained (takes 5-10 minutes). Subsequent runs will load the saved model instantly.

## 🌐 Deployment

This project is ready for free deployment! See `DEPLOYMENT_GUIDE.md` for detailed instructions.

**Quick Deploy Options:**
- **Render.com** (Recommended - No credit card needed)
- **Railway.app** (Fast deployments)
- **Fly.io** (Always-on free tier)
- **PythonAnywhere** (Beginner-friendly)

All deployment configuration files are included:
- `Procfile` - For deployment platforms
- `runtime.txt` - Python version specification
- `.gitignore` - Excludes model files from git
Dataset
The project uses a movie dataset containing columns like:
•	movie: Movie title
•	director: Director of the movie
•	genres: Movie genres (pipe-separated)
•	year: Release year
•	rating: IMDb or other ratings
•	revenue: Revenue generated
•	overview: Short description of the movie
•	duration: Length of the movie
Dataset Preprocessing:
•	Missing values are dropped.
•	Categorical columns like movie, genres, and director are encoded using LabelEncoder.
•	Genres are split into lists for calculating overlaps.

Model Overview
The recommendation model is built using Matrix Factorization with embeddings:
•	Inputs: Encoded movie and genre indices.
•	Embeddings: 
o	Movies: 50-dimensional
o	Genres: 10-dimensional
•	Dense Layers: 
o	64 hidden units with ReLU activation
o	Final output layer predicts movie ratings.
The model is trained for 10 epochs using mean_squared_error loss and the Adam optimizer.

Architecture
Components
Data Preprocessing: Cleans, integrates, and encodes metadata (genres, directors, ratings, revenue).

Content-Based Filtering (CBF): Uses similarity (TF-IDF + cosine similarity) on movie metadata.

Collaborative Filtering (CF): Matrix factorization with embeddings to capture hidden user–movie interactions.

Hybrid Engine: Combines results of CBF and CF for robust recommendations.

Analytics Module: Provides visual insights (genre distribution, revenue trends, director performance).

Flask Web App: Interactive user interface for recommendations.

Application Workflow
1.	User enters a movie title on the homepage.
2.	The app fetches the movie's attributes (e.g., genres, director).
3.	The model predicts ratings for all other movies.
4.	Recommendations are filtered based on: 
o	Genre overlap
o	Same director or year
o	High ratings
5.	Recommended movies are displayed with details and reasons.

File Descriptions
1. app.py
•	Main Flask application file.
•	Contains routes for the homepage (/) and recommendation logic (/recommend).
•	Defines the recommendation logic and uses the trained model for predictions.
2. analysis.py
•	Contains data analysis and visualization scripts.
•	Generates insights like: 
o	Genre frequency distribution.
o	Revenue trends by genre and director.
o	Yearly performance of movies.
o	Correlation between ratings and revenue.
3. templates/
•	index.html: Homepage with a search bar for entering movie titles.
•	recommendation.html: Displays movie recommendations.
•	error.html: Error page when no recommendations are found.
4. static/
•	images and other static assets used by the web application.
5. final_final_dataset.csv
•	Dataset file used for training and analysis.
Usage
1.	Run the Flask app using: 
2.	python app.py
3.	Enter a movie name in the search bar.
4.	View recommendations with reasons in the results page.

Analysis & Visualizations
1. Genre Frequency Distribution

2. Average Revenue by Genre

3. Director Success by Revenue

4. Year-wise Trends (Ratings & Revenue)

5. Correlation Heatmap

6. Impact of Duration on Ratings

Future Enhancements
•	Integrate user-based and item-based collaborative filtering.
•	Allow users to rate recommendations for improved personalization.
•	Extend the analysis to include actor-level insights.
•	Add more advanced NLP-based techniques to analyze movie overviews.

## Contributor
**Jayateja Alugolu**