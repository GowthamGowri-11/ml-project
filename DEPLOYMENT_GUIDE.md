# 🚀 Deployment Guide - Student Performance Predictor

## ✅ Issues Fixed

1. ✅ Created `streamlit_app.py` entry point for Streamlit Cloud
2. ✅ Restored `app.py` from backup
3. ✅ App running locally on port 8502

---

## 🌐 Local Access

Your app is now running at:
- **Local**: http://localhost:8502
- **Network**: http://192.168.31.163:8502
- **External**: http://157.51.112.185:8502

---

## ☁️ Streamlit Cloud Deployment

### Step 1: Fix the Main File Path

In your Streamlit Cloud deployment settings, you have two options:

#### Option A: Use streamlit_app.py (Recommended)
1. Keep "Main file path" as: `streamlit_app.py`
2. This file is already created and will import your main app

#### Option B: Change to app.py
1. Change "Main file path" to: `app.py`
2. This directly runs your main application file

### Step 2: Verify Repository Settings

Make sure these are correct:
```
Repository: GowthamGowri-11/ml-project
Branch: main
Main file path: streamlit_app.py  (or app.py)
```

### Step 3: Deploy

Click the **"Deploy"** button at the bottom of the page.

---

## 📁 Required Files for Deployment

Make sure these files are in your GitHub repository:

### Essential Files
- ✅ `streamlit_app.py` - Entry point (newly created)
- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `train_new_dataset.py` - Model training script

### Data Files
- ✅ `dataset/Student_performance_data _.csv` - Training data
- ✅ `models/best_model.joblib` - Trained model
- ✅ `models/preprocessor.joblib` - Data preprocessor
- ✅ `models/model_metadata.json` - Model info

### Source Code
- ✅ `src/__init__.py`
- ✅ `src/predict.py`
- ✅ `src/preprocessing.py`
- ✅ `src/train.py`
- ✅ `src/utils.py`

---

## 🔧 Common Deployment Issues & Solutions

### Issue 1: "File does not exist: streamlit_app.py"
**Solution**: 
- The file is now created! Just commit and push to GitHub
- Or change Main file path to `app.py`

### Issue 2: "Module not found"
**Solution**: 
- Check `requirements.txt` has all dependencies
- Current requirements:
```
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
joblib>=1.3.0
plotly>=5.0.0
```

### Issue 3: "Model files not found"
**Solution**: 
- Make sure `models/` folder is in GitHub
- Run `python train_new_dataset.py` to generate models
- Commit and push the models folder

### Issue 4: "Port already in use" (Local)
**Solution**: 
- Use different port: `streamlit run app.py --server.port 8502`
- Or kill existing process: `Get-Process streamlit | Stop-Process`

---

## 📦 Git Commands to Deploy

### 1. Add all files
```bash
git add .
```

### 2. Commit changes
```bash
git commit -m "Add streamlit_app.py entry point and fix deployment"
```

### 3. Push to GitHub
```bash
git push origin main
```

### 4. Streamlit Cloud will auto-deploy
Once pushed, Streamlit Cloud will automatically detect changes and redeploy.

---

## 🎯 Deployment Checklist

Before deploying, verify:

- [ ] `streamlit_app.py` exists
- [ ] `app.py` exists and works locally
- [ ] `requirements.txt` is complete
- [ ] Model files are in `models/` folder
- [ ] Dataset is in `dataset/` folder
- [ ] All source files are in `src/` folder
- [ ] `.gitignore` excludes `__pycache__`
- [ ] Repository is public or you have Streamlit Cloud access
- [ ] Branch name is correct (main)
- [ ] Main file path is correct

---

## 🌐 After Deployment

### Your app will be available at:
```
https://students-performance-predictor-gg.streamlit.app
```
(or similar URL provided by Streamlit Cloud)

### Features that will work:
✅ All 4 tabs (Predict, Data Explorer, Model Performance, About)
✅ Theme switching (Dark/Light mode)
✅ All visualizations and charts
✅ Model predictions
✅ Data filtering and exploration
✅ All animations and effects

---

## 🔍 Monitoring Deployment

### Check deployment status:
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View logs in real-time
4. Check for any errors

### Common deployment logs:
```
✅ Building app...
✅ Installing dependencies...
✅ Starting app...
✅ App is live!
```

---

## 🎨 Custom Domain (Optional)

If you want a custom domain:

1. Go to app settings in Streamlit Cloud
2. Click "Custom domain"
3. Follow instructions to set up DNS
4. Example: `students-predictor.yourdomain.com`

---

## 📊 Performance Tips for Cloud

### Optimize for cloud deployment:

1. **Cache data loading**
```python
@st.cache_data
def load_data():
    return pd.read_csv("dataset/Student_performance_data _.csv")
```

2. **Cache model loading**
```python
@st.cache_resource
def load_model():
    return joblib.load("models/best_model.joblib")
```

3. **Reduce file sizes**
- Compress images
- Minimize dataset if possible
- Use efficient data formats

---

## 🔐 Security Best Practices

### For production deployment:

1. **Don't commit sensitive data**
   - Use Streamlit secrets for API keys
   - Add `.env` to `.gitignore`

2. **Validate user inputs**
   - Already implemented in the app
   - Check ranges and types

3. **Rate limiting**
   - Streamlit Cloud handles this automatically

---

## 🆘 Troubleshooting

### If deployment fails:

1. **Check logs** in Streamlit Cloud
2. **Verify all files** are committed
3. **Test locally** first
4. **Check requirements.txt** versions
5. **Ensure Python version** compatibility

### Get help:
- Streamlit Community Forum
- GitHub Issues
- Streamlit Documentation

---

## 📞 Quick Commands Reference

### Local Development
```bash
# Run app
streamlit run app.py

# Run on different port
streamlit run app.py --server.port 8502

# Train model
python train_new_dataset.py

# Run tests
python run_tests.py
```

### Git Commands
```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull latest
git pull origin main
```

---

## ✅ Final Steps

1. **Commit the new streamlit_app.py**
```bash
git add streamlit_app.py
git commit -m "Add Streamlit Cloud entry point"
git push origin main
```

2. **Go to Streamlit Cloud**
   - Refresh the deployment page
   - Click "Deploy" button
   - Wait for deployment to complete

3. **Test your deployed app**
   - Visit the provided URL
   - Test all features
   - Switch themes
   - Make predictions

---

## 🎉 Success!

Once deployed, your premium Student Performance Predictor will be:
- ✅ Accessible worldwide
- ✅ Always online
- ✅ Auto-updating from GitHub
- ✅ Free to use (Streamlit Community Cloud)

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)

---

**Your app is ready to deploy!** 🚀

**Current Status**:
- ✅ Local app running: http://localhost:8502
- ✅ Entry point created: streamlit_app.py
- ✅ Main app restored: app.py
- ✅ All files ready for deployment

**Next Step**: Push to GitHub and deploy on Streamlit Cloud!

---

*Deployment Guide - Version 1.0*
*Last Updated: April 9, 2026*
