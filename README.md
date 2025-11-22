# 🎵 musicai - AI-Powered Music Discovery

[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)](https://www.sqlite.org/)

musicai - is an intelligent music recommendation system that uses AI to analyze your music taste and suggest personalized tracks. It combines the power of Gemini AI for smart recommendations with Spotify's extensive music catalog.

## ✨ Features

- 🎯 **Smart Recommendations**: AI-powered song suggestions based on your playlist
- 🔄 **Playlist Import**: Easy import from Spotify playlists
- 📊 **Discovery Stats**: Track your music exploration journey
- 💾 **Persistent Storage**: Your music preferences are saved between sessions
- 🎨 **Modern UI**: Clean, responsive interface with loading states

## 🏗 Architecture

### Frontend (React)
- Modern React with hooks for state management
- Real-time loading states and animations
- Responsive design for all devices
- Statistics visualization

### Backend (Flask)
- RESTful API architecture
- Gemini AI integration for recommendations
- Spotify API integration for music data
- Efficient caching and error handling
- Comprehensive API documentation

### Database (SQLite)
- Persistent storage for songs and preferences
- Stores imported songs, recommendations, and playlists
- Automatic schema migrations
- Efficient querying and indexing

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Spotify Developer Account
- Gemini AI API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Roots26Hz/musicai.git
cd musicai
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Spotify and Gemini AI credentials
```

4. Set up the frontend:
```bash
cd ../frontend/ai-music-recommender
npm install
```

5. Start the servers:

Backend:
```bash
cd ../../backend
python app.py
```

Frontend:
```bash
cd ../frontend/ai-music-recommender
npm start
```

Visit `http://localhost:3000` to see the app in action!

## 📊 Data Flow

1. **Playlist Import**
   - Frontend sends playlist URL to backend
   - Backend fetches songs from Spotify
   - Songs stored in SQLite database

2. **Recommendation Generation**
   - Imported songs analyzed by Gemini AI
   - Recommendations generated and stored
   - Results cached for performance

3. **Playlist Building**
   - User selections saved to database
   - Automatic sync between sessions
   - Real-time updates across components

## 🛠 Tech Stack

- **Frontend**: React, CSS3, Lucide Icons
- **Backend**: Flask, SQLAlchemy, Python
- **Database**: SQLite
- **APIs**: Spotify Web API, Gemini AI
- **Tools**: Node.js, pip, npm

## 📝 API Documentation

### Endpoints

- `POST /api/import` - Import playlist
- `POST /api/recommend` - Generate recommendations
- `GET /api/stored/imported` - Get stored songs
- `GET /api/stored/recommendations` - Get recommendations
- `GET/POST /api/stored/playlist` - Manage built playlist
- `POST /api/stats` - Calculate statistics

Full API documentation available in [API.md](./API.md)


## Acknowledgments

- Spotify Web API for music data
- Gemini AI for smart recommendations
- React community for awesome tools
- Flask team for the robust backend framework

## Future Enhancements

- 🎤 Voice-based song search and recommendations
- 📱 Mobile app support (React Native)
- 🧠 Advanced AI models for deeper personalization
- 🌐 Multi-language support for global users
- 🔔 Push notifications for new recommendations
- 🛡️ Enhanced privacy controls and data export
- 🏆 Gamification and achievement badges



## 📫 Contact

- GitHub: [@Roots26Hz](https://github.com/Roots26Hz)
- Project Link: [https://github.com/Roots26Hz/musicai](https://github.com/Roots26Hz/musicai)
