# 🔄 How to Rename Your Render Service to "AJT CineMatch"

## Step-by-Step Instructions

### 1. Go to Render Dashboard
- Log in to https://render.com
- Navigate to your dashboard

### 2. Find Your Web Service
- Click on your current service: `movie-recommendation-analysis-using-data`

### 3. Rename the Service
- Click on **"Settings"** tab (in the left sidebar)
- Scroll down to **"Name"** section
- Change the name from:
  - **Current:** `movie-recommendation-analysis-using-data`
  - **New:** `ajt-cinematch`
- Click **"Save Changes"**

### 4. Wait for Update
- Render will automatically update the URL
- Your new URL will be: `https://ajt-cinematch.onrender.com`
- This may take a few minutes

### 5. Verify the New URL
- Once updated, visit: `https://ajt-cinematch.onrender.com`
- Make sure everything works correctly

## ⚠️ Important Notes

1. **Old URL will stop working** - The old URL (`movie-recommendation-analysis-using-data.onrender.com`) will no longer work after renaming.

2. **DNS Propagation** - It may take a few minutes for the new URL to be fully active.

3. **GitHub Connection** - Your GitHub connection will remain intact, only the service name changes.

4. **Environment Variables** - All your environment variables and settings will be preserved.

5. **Deployments** - Future deployments will use the new URL automatically.

## ✅ Files Already Updated

I've already updated all your files to use the new URL:
- ✅ `static/sitemap.xml` - Updated to `ajt-cinematch.onrender.com`
- ✅ `static/robots.txt` - Updated to `ajt-cinematch.onrender.com`
- ✅ `templates/index.html` - All meta tags updated
- ✅ `templates/recommendations.html` - All meta tags updated
- ✅ `templates/error.html` - All meta tags updated

## 🚀 After Renaming

1. **Commit and push the updated files:**
   ```bash
   git add static/ templates/
   git commit -m "Update URLs to ajt-cinematch.onrender.com"
   git push
   ```

2. **Update Google Search Console:**
   - Add the new property: `ajt-cinematch.onrender.com`
   - Submit the new sitemap: `https://ajt-cinematch.onrender.com/sitemap.xml`
   - Set up 301 redirects if needed (optional)

3. **Test Everything:**
   - Visit the new URL
   - Test the search functionality
   - Check robots.txt: `https://ajt-cinematch.onrender.com/robots.txt`
   - Check sitemap: `https://ajt-cinematch.onrender.com/sitemap.xml`

## Alternative URL Options

If `ajt-cinematch` is taken, you can try:
- `ajt-cinematch-app`
- `ajtcinematch`
- `ajts-cinematch`
- `ajt-movie-recommender`

Just let me know and I'll update all files with your chosen name!

## 🎉 Result

After renaming, your site will be accessible at:
**https://ajt-cinematch.onrender.com**

Much better branding for "AJT's CineMatch"! 🎬

