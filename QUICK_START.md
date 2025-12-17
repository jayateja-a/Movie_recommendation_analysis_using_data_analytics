# Quick Start Guide

## 🚀 Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   - Navigate to: `http://localhost:5000`
   - Enter a movie name and get recommendations!

## 📝 First Run Notes

- **First time:** The app will train the model (takes 5-10 minutes)
- **Subsequent runs:** Model loads instantly from saved files
- **Model files created:**
  - `movie_recommendation_model.h5` - Trained model
  - `encoders.pkl` - Label encoders

## 🌐 Deploying Online

See `DEPLOYMENT_GUIDE.md` for detailed instructions on deploying to free hosting platforms.

**Recommended:** Use **Render.com** for easiest deployment!

## 🎬 Testing

Try these movie names (if they're in your dataset):
- Any movie from your `final_final_dataset.csv`
- The app will show recommendations based on genre, director, and year

## ⚠️ Troubleshooting

**Import errors:**
- Make sure all packages are installed: `pip install -r requirements.txt`

**Model training takes long:**
- This is normal on first run
- Model is saved for future use

**No recommendations found:**
- Make sure the movie name matches exactly as in your dataset
- Check that `final_final_dataset.csv` is in the project directory

