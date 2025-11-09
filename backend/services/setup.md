# Step 2: Backend Setup Guide - Flask + Gemini AI

## Overview
This guide will help you set up a Python Flask backend with Google Gemini 2.5 Pro for AI recommendations, and connect it to your React frontend.

---

## Part A: Initial Backend Setup

### 1. Create Backend Directory Structure

In your project root (where `music-recommendation-engine` folder exists), create a new backend folder:

```bash
# Navigate to your project parent directory
cd path/to/your/projects

# Create backend directory
mkdir music-recommendation-backend
cd music-recommendation-backend
```

Your structure should look like:
```
your-projects/
â”œâ”€â”€ music-recommendation-engine/  (React frontend)
â””â”€â”€ music-recommendation-backend/ (Flask backend) â† You are here
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You'll see `(venv)` in your terminal when activated.

### 3. Install Required Dependencies

```bash
pip install flask flask-cors google-generativeai python-dotenv requests
```

**What each does:**
- `flask` - Web framework for API
- `flask-cors` - Handles cross-origin requests from React
- `google-generativeai` - Gemini AI SDK
- `python-dotenv` - Manages environment variables
- `requests` - HTTP library for API calls

### 4. Create requirements.txt

```bash
pip freeze > requirements.txt
```

---

## Part B: Get API Keys

### 1. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key" or "Create API Key"
3. Copy your API key (starts with `AIza...`)

### 2. Get Apple Music API Credentials

1. Go to [Apple Developer Portal](https://developer.apple.com/)
2. Sign in with Apple ID
3. Navigate to "Certificates, Identifiers & Profiles"
4. Create MusicKit identifier and keys
5. Note: This requires Apple Developer Program ($99/year)

**Alternative for development:** Use Spotify API (free)
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Copy Client ID and Client Secret

---

## Part C: Create Backend Files

### 1. Create `.env` file (in `music-recommendation-backend/`)

```bash
# Create .env file
touch .env
```

**Add to `.env`:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
FLASK_ENV=development
```

âš ï¸ **Important:** Add `.env` to `.gitignore`

### 2. Create `.gitignore`

```bash
# Create .gitignore
touch .gitignore
```

**Add to `.gitignore`:**
```
venv/
__pycache__/
*.pyc
.env
.DS_Store
*.db
```

### 3. Create `app.py` (Main Flask Application)

Create this file and copy the content I'll provide in the next artifact.

### 4. Create `services/` directory

```bash
mkdir services
touch services/__init__.py
touch services/gemini_service.py
touch services/spotify_service.py
```

---

## Part D: Project Structure

Your backend should look like this:

```
music-recommendation-backend/
â”œâ”€â”€ venv/                    # Virtual environment (not in git)
â”œâ”€â”€ services/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ gemini_service.py   # AI recommendation logic
â”‚   â””â”€â”€ spotify_service.py  # Spotify API integration
â”œâ”€â”€ .env                     # Environment variables (not in git)
â”œâ”€â”€ .gitignore
â”œâ”€â”€ app.py                   # Main Flask app
â””â”€â”€ requirements.txt
```

---

## Part E: Run the Backend

### 1. Make sure virtual environment is activated

```bash
# You should see (venv) in terminal
# If not, activate it:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

### 2. Run Flask server

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

### 3. Test the API

Open browser or use curl:
```bash
curl http://localhost:5000/api/health
```

Should return: `{"status": "healthy"}`

---

## Part F: Connect React Frontend to Backend

### 1. Update React App to Use Backend

In your React project (`music-recommendation-engine/`), create a new file:

```bash
# In music-recommendation-engine/src/
touch api.js
```

**Add to `src/api.js`:**
```javascript
const API_BASE_URL = 'http://localhost:5000/api';

export const importPlaylist = async (playlistUrl) => {
  const response = await fetch(`${API_BASE_URL}/import`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ playlistUrl }),
  });
  return response.json();
};

export const generateRecommendations = async (songs) => {
  const response = await fetch(`${API_BASE_URL}/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ songs }),
  });
  return response.json();
};
```

### 2. Update `App.js` to use API

Find the `handleImportPlaylist` function and update:

```javascript
import { importPlaylist, generateRecommendations } from './api';

// Update handleImportPlaylist
const handleImportPlaylist = async (e) => {
  e.preventDefault();
  try {
    const data = await importPlaylist(playlistUrl);
    setImportedSongs(data.songs);
    setActiveTab('imported');
  } catch (error) {
    console.error('Error importing playlist:', error);
    alert('Failed to import playlist. Make sure backend is running.');
  }
};

// Update handleGenerateRecommendations
const handleGenerateRecommendations = async () => {
  try {
    const data = await generateRecommendations(importedSongs);
    setRecommendations(data.recommendations);
    setActiveTab('recommendations');
  } catch (error) {
    console.error('Error generating recommendations:', error);
    alert('Failed to generate recommendations.');
  }
};
```

---

## Part G: Test the Full Stack

### 1. Start Backend (Terminal 1)

```bash
cd music-recommendation-backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

### 2. Start Frontend (Terminal 2)

```bash
cd music-recommendation-engine
npm start
```

### 3. Test the Flow

1. Open `http://localhost:3000`
2. Paste a Spotify playlist URL (e.g., `https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`)
3. Click "Import Playlist"
4. Click "Generate Recommendations"
5. See AI-powered recommendations!

---

## Part H: GitHub Repository Setup

### 1. Initialize Backend Git

```bash
cd music-recommendation-backend
git init
git add .
git commit -m "Initial backend setup with Flask and Gemini"
```

### 2. Push to GitHub

**Option 1: Separate Repository (Recommended)**
```bash
# Create new repo on GitHub for backend
git remote add origin https://github.com/YOUR_USERNAME/music-recommendation-backend.git
git branch -M main
git push -u origin main
```

**Option 2: Monorepo (Both in one repo)**
```bash
# Move backend into frontend repo
mv music-recommendation-backend music-recommendation-engine/backend
cd music-recommendation-engine
git add backend/
git commit -m "Add Flask backend with Gemini integration"
git push
```

---

## Part I: Development Workflow

### Daily Development

**Terminal 1 - Backend:**
```bash
cd music-recommendation-backend
source venv/bin/activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd music-recommendation-engine
npm start
```

### Adding New Python Packages

```bash
pip install package-name
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add package-name dependency"
```

---

## Troubleshooting

### Issue: "Module not found" errors
**Solution:** Make sure virtual environment is activated
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Issue: CORS errors in browser
**Solution:** Make sure Flask-CORS is installed and configured in `app.py`

### Issue: "Connection refused" from React
**Solution:** 
1. Check backend is running on port 5000
2. Verify `API_BASE_URL` in `api.js` is correct

### Issue: Gemini API errors
**Solution:**
1. Verify API key in `.env` is correct
2. Check [API quota](https://makersuite.google.com/app/apikey)
3. Ensure no extra spaces in `.env` file

---

## Next Steps

1. âœ… Backend running on `http://localhost:5000`
2. âœ… Frontend running on `http://localhost:3000`
3. âœ… Both connected and communicating
4. ðŸ”„ Implement music metadata extraction
5. ðŸ”„ Enhance AI recommendation logic
6. ðŸ”„ Add Apple Music API integration

---

## Useful Commands Cheatsheet

```bash
# Activate virtual environment
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Deactivate virtual environment
deactivate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Run Flask in development mode
python app.py

# Check installed packages
pip list

# Update requirements.txt
pip freeze > requirements.txt
```

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [Flask-CORS Guide](https://flask-cors.readthedocs.io/)