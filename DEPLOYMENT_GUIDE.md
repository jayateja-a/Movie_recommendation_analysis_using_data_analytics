# 🚀 Free Deployment Guide for Movie Recommendation System

This guide will help you deploy your Movie Recommendation System to the internet for **FREE** using various hosting platforms.

## 📋 Prerequisites

1. **Git** installed on your computer
2. **GitHub account** (free) - https://github.com
3. Your project files ready

## 🎯 Recommended Free Hosting Platforms

### Option 1: **Render** (⭐ RECOMMENDED - Easiest & Most Reliable)

**Why Render?**
- ✅ Completely free tier available
- ✅ Automatic deployments from GitHub
- ✅ No credit card required
- ✅ Easy setup
- ✅ Free SSL certificate
- ✅ Custom domain support

**Limitations:**
- Free tier spins down after 15 minutes of inactivity (takes ~30 seconds to wake up)
- 750 hours/month free (enough for personal projects)

**Steps to Deploy:**

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/movie-recommendation-system.git
   git push -u origin main
   ```

2. **Create Render Account:**
   - Go to https://render.com
   - Sign up with GitHub (free)

3. **Deploy on Render:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** movie-recommendation-system (or any name)
     - **Environment:** Python 3
     - **Python Version:** 3.11.9 (set in Environment Variables if available, or ensure runtime.txt is present)
     - **Build Command:** `pip install --upgrade pip setuptools wheel && pip install --only-binary :all: -r requirements.txt || pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free
     - **Environment Variables (optional but recommended):**
       - `PYTHON_VERSION=3.11.9`
       - `PIP_ONLY_BINARY=:all:` (forces use of pre-built wheels)
   - Click "Create Web Service"
   - Wait for deployment (first time takes 5-10 minutes to train model)

4. **Your app will be live at:** `https://your-app-name.onrender.com`

---

### Option 2: **Railway** (Great Alternative)

**Why Railway?**
- ✅ $5 free credit monthly (enough for small projects)
- ✅ No spin-down (always on)
- ✅ Very fast deployments
- ✅ Easy to use

**Limitations:**
- Requires credit card (but won't charge if you stay within free tier)
- $5 credit = ~500 hours/month

**Steps to Deploy:**

1. **Push code to GitHub** (same as Render step 1)

2. **Create Railway Account:**
   - Go to https://railway.app
   - Sign up with GitHub
   - Add payment method (won't charge if within free tier)

3. **Deploy:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Flask apps
   - Add environment variable: `PORT=5000` (if needed)
   - Your app deploys automatically!

4. **Your app will be live at:** `https://your-app-name.up.railway.app`

---

### Option 3: **Fly.io** (Good for Always-On Apps)

**Why Fly.io?**
- ✅ Free tier with 3 shared VMs
- ✅ No spin-down
- ✅ Global edge network
- ✅ Good performance

**Limitations:**
- Slightly more complex setup
- Need to install Fly CLI

**Steps to Deploy:**

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login to Fly:**
   ```bash
   fly auth signup
   ```

3. **Initialize Fly in your project:**
   ```bash
   fly launch
   ```
   - Follow prompts
   - Don't deploy a Postgres database (not needed)
   - Choose a region close to you

4. **Deploy:**
   ```bash
   fly deploy
   ```

5. **Your app will be live at:** `https://your-app-name.fly.dev`

---

### Option 4: **PythonAnywhere** (Simple & Beginner-Friendly)

**Why PythonAnywhere?**
- ✅ Free tier available
- ✅ No credit card needed
- ✅ Easy web interface
- ✅ Good for learning

**Limitations:**
- Free tier has limited resources
- Only accessible from whitelisted domains
- Can be slow

**Steps to Deploy:**

1. **Create Account:**
   - Go to https://www.pythonanywhere.com
   - Sign up for free "Beginner" account

2. **Upload Files:**
   - Go to "Files" tab
   - Upload all your project files
   - Make sure `final_final_dataset.csv` is uploaded

3. **Open Bash Console:**
   - Install dependencies:
     ```bash
     pip3.10 install --user flask tensorflow pandas numpy scikit-learn gunicorn
     ```

4. **Create Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask
   - Python version: 3.10
   - Enter path to your `app.py`

5. **Configure:**
   - Set WSGI file to point to your app
   - Reload web app

6. **Your app will be live at:** `https://YOUR_USERNAME.pythonanywhere.com`

---

### Option 5: **Hugging Face Spaces** (If you convert to Gradio/Streamlit)

**Why Hugging Face?**
- ✅ Completely free
- ✅ No credit card
- ✅ Great for ML projects
- ✅ Easy sharing

**Note:** Would require converting Flask app to Streamlit or Gradio

---

## 🔧 Important Configuration Notes

### For All Platforms:

1. **Make sure these files exist:**
   - ✅ `requirements.txt` (fixed)
   - ✅ `Procfile` (created)
   - ✅ `runtime.txt` (created)
   - ✅ `.gitignore` (created)

2. **First Deployment:**
   - The first deployment will take longer (5-10 minutes) because it needs to train the model
   - Subsequent deployments will be faster (model is saved)

3. **File Size:**
   - Make sure `final_final_dataset.csv` is uploaded to your repository
   - If it's too large (>100MB), consider using Git LFS or hosting it separately

4. **Environment Variables (if needed):**
   - Most platforms auto-detect Flask apps
   - If needed, set `PORT` environment variable

---

## 🎯 My Recommendation

**For your project, I recommend Render** because:
1. ✅ Easiest setup
2. ✅ No credit card required
3. ✅ Automatic deployments
4. ✅ Free SSL
5. ✅ Good documentation

The 15-minute spin-down is fine for a personal project - it just takes 30 seconds to wake up when someone visits.

---

## 📝 Quick Start Checklist

- [ ] Push code to GitHub
- [ ] Create account on chosen platform
- [ ] Connect GitHub repository
- [ ] Configure build/start commands
- [ ] Deploy!
- [ ] Test your live URL
- [ ] Share with friends! 🎉

---

## 🐛 Troubleshooting

### App crashes on startup:
- Check logs in your hosting platform
- Ensure all dependencies are in `requirements.txt`
- Verify `final_final_dataset.csv` is in the repository

### TensorFlow version errors:
- If you see "Could not find a version that satisfies the requirement tensorflow==X.X.X":
  - The `requirements.txt` has been updated to use TensorFlow 2.20.0 (latest available)
  - Make sure you've pulled the latest changes from GitHub
  - If issues persist, try: `tensorflow>=2.14.0` (flexible version)

### Model training takes too long:
- First deployment always takes longer
- Model is saved after first training, so subsequent deployments are faster

### "Module not found" errors:
- Check `requirements.txt` has all packages
- Ensure correct Python version in `runtime.txt`

### Port errors:
- Most platforms set PORT automatically
- If needed, use: `port = int(os.environ.get('PORT', 5000))` (already in app.py)

### Build fails:
- Check the build logs for specific error messages
- Ensure Python version in `runtime.txt` is compatible (3.11.5)
- Try clearing build cache on Render and redeploying
- **Pandas compilation errors:** The build command now upgrades pip first, which helps install pre-built wheels. If you still see compilation errors:
  - Make sure build command is: `pip install --upgrade pip && pip install -r requirements.txt`
  - The updated requirements.txt uses newer versions with pre-built wheels

---

## 🎉 Success!

Once deployed, your Movie Recommendation System will be accessible to anyone on the internet!

**Share your deployed URL and enjoy your live project!**

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Fly.io Docs: https://fly.io/docs

