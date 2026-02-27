# How to Share Your Stock Prediction Backend 📤

## Option 1: GitHub (Recommended) 🌟

### Step 1: Initialize Git Repository
```bash
cd ~/Desktop/stock-ai-backend
git init
git add .
git commit -m "Initial commit: Production-ready stock prediction API v2.1"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `stock-ai-backend`
3. Description: "Production-ready stock prediction API with ML models"
4. Choose Public or Private
5. Click "Create repository"

### Step 3: Push to GitHub
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/stock-ai-backend.git
git branch -M main
git push -u origin main
```

### Step 4: Share the Link
Send your frontend partner:
```
https://github.com/YOUR_USERNAME/stock-ai-backend
```

---

## Option 2: ZIP File 📦

### Create ZIP Archive
```bash
cd ~/Desktop
zip -r stock-ai-backend.zip stock-ai-backend/ \
  -x "*.pyc" \
  -x "*__pycache__*" \
  -x "*.pth" \
  -x "*.pkl" \
  -x "*venv*" \
  -x "*.DS_Store"
```

### Share via:
- **Email**: Attach `stock-ai-backend.zip`
- **Google Drive**: Upload and share link
- **Dropbox**: Upload and share link
- **WeTransfer**: https://wetransfer.com

---

## Option 3: Deploy Online (For Testing) 🌐

### A. Deploy to Render (Free)

1. **Create account**: https://render.com
2. **New Web Service**
3. **Connect GitHub repo** (from Option 1)
4. **Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Deploy**

Your API will be live at: `https://your-app.onrender.com`

### B. Deploy to Railway (Free)

1. **Create account**: https://railway.app
2. **New Project** → **Deploy from GitHub**
3. **Select your repo**
4. **Add environment variables** from `.env`
5. **Deploy**

Your API will be live at: `https://your-app.railway.app`

### C. Deploy to Heroku

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create your-stock-api

# Deploy
git push heroku main

# Open
heroku open
```

---

## Option 4: Local Network Sharing 🏠

### Share on Same WiFi Network

1. **Find your IP address**:
```bash
# macOS
ipconfig getifaddr en0

# Example output: 192.168.1.100
```

2. **Start server on all interfaces**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. **Share with your partner**:
```
http://192.168.1.100:8000
```

They can access from their computer on the same WiFi!

---

## What to Share with Your Frontend Partner 📋

### Essential Information

**1. API Base URL**:
- Local: `http://localhost:8000`
- Deployed: `https://your-app.onrender.com`

**2. Key Endpoints**:
```
GET  /api/v1/predict?symbol=AAPL
POST /api/v1/predict/batch
GET  /health
GET  /metrics
GET  /docs
```

**3. Documentation**:
- Interactive Docs: `{BASE_URL}/docs`
- Frontend Guide: `FRONTEND_GUIDE.md`
- Quick Start: `QUICKSTART.md`

**4. Example Request**:
```javascript
fetch('http://localhost:8000/api/v1/predict?symbol=AAPL')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Recommended Sharing Package 📦

### Create a README for Your Partner

```bash
cat > PARTNER_README.md << 'EOF'
# Stock Prediction API - Frontend Integration

## Quick Start

1. Clone/Download this repository
2. Install dependencies: `pip3 install -r requirements.txt`
3. Start server: `uvicorn app.main:app --reload`
4. API runs at: `http://localhost:8000`

## API Documentation

Interactive docs: http://localhost:8000/docs

## Key Endpoints

### Single Prediction
GET /api/v1/predict?symbol=AAPL

### Batch Prediction
POST /api/v1/predict/batch
Body: {"symbols": ["AAPL", "GOOGL", "MSFT"]}

### Health Check
GET /health

## Frontend Integration

See FRONTEND_GUIDE.md for React/JavaScript examples.

## Support

- API Docs: http://localhost:8000/docs
- Questions? Check QUICKSTART.md
EOF
```

---

## GitHub Repository Setup (Detailed) 🔧

### 1. Create `.gitignore` (Already done!)
```
__pycache__/
*.pyc
*.pth
*.pkl
.env
venv/
.DS_Store
```

### 2. Add README.md (Already done!)

### 3. Optional: Add GitHub Actions for CI/CD

Create `.github/workflows/test.yml`:
```yaml
name: Test API

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python test_api.py
```

---

## Sharing Checklist ✅

Before sharing, make sure:

- [ ] All files are saved
- [ ] Models are trained (`app/models/` has .pth and .pkl files)
- [ ] `.env` file has correct API key
- [ ] `README.md` is up to date
- [ ] Tests pass (`python3 test_api.py`)
- [ ] Server starts successfully
- [ ] Documentation is complete

---

## Quick Commands Reference 📝

```bash
# Initialize Git
git init
git add .
git commit -m "Initial commit"

# Create ZIP
zip -r stock-ai-backend.zip stock-ai-backend/

# Start server
uvicorn app.main:app --reload

# Test API
python3 test_api.py

# Check files
ls -la

# View docs
open http://localhost:8000/docs
```

---

## Recommended Approach 🎯

**For Frontend Partner:**
1. ✅ Push to GitHub (best for collaboration)
2. ✅ Share GitHub link
3. ✅ Point them to `/docs` for API documentation
4. ✅ Share `FRONTEND_GUIDE.md`

**For Demo/Testing:**
1. ✅ Deploy to Render or Railway (free)
2. ✅ Share live URL
3. ✅ They can test immediately without setup

**For Quick Share:**
1. ✅ Create ZIP file
2. ✅ Upload to Google Drive/Dropbox
3. ✅ Share link

---

## Example Email to Frontend Partner 📧

```
Subject: Stock Prediction API - Ready for Integration!

Hi [Name],

The stock prediction backend is ready! 🎉

GitHub: https://github.com/YOUR_USERNAME/stock-ai-backend
Live Demo: https://your-app.onrender.com (if deployed)

Quick Start:
1. Clone the repo
2. Run: pip3 install -r requirements.txt
3. Run: uvicorn app.main:app --reload
4. API at: http://localhost:8000

Documentation:
- Interactive API Docs: http://localhost:8000/docs
- Frontend Guide: See FRONTEND_GUIDE.md in the repo
- Quick Start: See QUICKSTART.md

Key Endpoints:
- GET /api/v1/predict?symbol=AAPL
- POST /api/v1/predict/batch
- GET /health

Features:
✅ Error handling
✅ Caching (53x faster)
✅ Batch predictions
✅ Health checks
✅ Metrics tracking

Let me know if you need any help!

Best,
[Your Name]
```

---

## Need Help? 🆘

### Common Issues

**"How do I get a GitHub account?"**
- Go to https://github.com/join
- Sign up for free

**"How do I install Git?"**
```bash
# macOS
brew install git

# Or download from: https://git-scm.com/downloads
```

**"Can I share without GitHub?"**
- Yes! Use ZIP file option or deploy online

**"How do I deploy for free?"**
- Render.com (recommended)
- Railway.app
- Heroku (requires credit card)

---

## Summary 📋

**Easiest**: GitHub → Share link
**Fastest**: ZIP file → Email/Drive
**Best for Demo**: Deploy to Render → Share URL
**Best for Development**: GitHub + Local server

Choose what works best for you! 🚀
