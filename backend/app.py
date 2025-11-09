from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from services.gemini_service import GeminiRecommendationEngine
from services.spotify_service import SpotifyService
from models import db, ImportedSong, Recommendation, BuiltPlaylist

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize services
gemini_engine = GeminiRecommendationEngine(api_key=os.getenv('GEMINI_API_KEY'))
spotify_service = SpotifyService(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({'status': 'healthy', 'message': 'Backend is running'}), 200

# Import playlist endpoint
@app.route('/api/import', methods=['POST'])
def import_playlist():
    """
    Import playlist from Spotify or Apple Music URL
    Expected JSON: { "playlistUrl": "https://..." }
    """
    try:
        data = request.get_json()
        playlist_url = data.get('playlistUrl')
        
        if not playlist_url:
            return jsonify({'error': 'Playlist URL is required'}), 400
        
        # Determine platform (Spotify or Apple Music)
        if 'spotify.com' in playlist_url:
            # Extract playlist from Spotify
            songs = spotify_service.get_playlist_tracks(playlist_url)
            
            if not songs:
                return jsonify({'error': 'Failed to fetch playlist or playlist is empty'}), 400
            
            # Clear existing imported songs
            ImportedSong.query.delete()
            
            # Store songs in database
            for song in songs:
                db_song = ImportedSong(
                    id=song['id'],
                    title=song['title'],
                    artist=song['artist'],
                    album=song.get('album', ''),
                    genre=song.get('genre', ''),
                    tempo=song.get('tempo', 0),
                    mood=song.get('mood', ''),
                    preview_url=song.get('preview_url', '')
                )
                db.session.add(db_song)
            
            db.session.commit()
                
            return jsonify({
                'success': True,
                'platform': 'spotify',
                'songs': songs,
                'count': len(songs)
            }), 200
            
        elif 'music.apple.com' in playlist_url:
            # Apple Music integration (placeholder for now)
            return jsonify({
                'error': 'Apple Music integration coming soon. Please use Spotify for now.',
                'info': 'Requires Apple Developer Program enrollment'
            }), 501
            
        else:
            return jsonify({'error': 'Unsupported playlist URL. Use Spotify or Apple Music.'}), 400
            
    except Exception as e:
        print(f"Error importing playlist: {str(e)}")
        return jsonify({'error': f'Failed to import playlist: {str(e)}'}), 500

# Generate recommendations endpoint
@app.route('/api/recommend', methods=['POST'])
def generate_recommendations():
    """
    Generate AI-powered recommendations based on imported songs
    Expected JSON: { "songs": [{id, title, artist, genre, tempo, mood}, ...] }
    """
    try:
        data = request.get_json()
        songs = data.get('songs', [])
        
        if not songs:
            return jsonify({'error': 'Songs array is required'}), 400
        
        # Generate recommendations using Gemini AI
        recommendations = gemini_engine.generate_recommendations(songs)
        
        if not recommendations:
            return jsonify({'error': 'Failed to generate recommendations'}), 500
        
        # Clear existing recommendations
        Recommendation.query.delete()
        
        # Store recommendations in database
        for rec in recommendations:
            db_rec = Recommendation(
                id=rec['id'],
                title=rec['title'],
                artist=rec['artist'],
                album=rec.get('album', ''),
                genre=rec.get('genre', ''),
                tempo=rec.get('tempo', 0),
                mood=rec.get('mood', ''),
                reason=rec.get('reason', ''),
                preview_url=rec.get('preview_url', '')
            )
            db.session.add(db_rec)
        
        db.session.commit()
            
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return jsonify({'error': f'Failed to generate recommendations: {str(e)}'}), 500

# Get mood-based recommendations
@app.route('/api/recommend/mood', methods=['POST'])
def mood_recommendations():
    """
    Generate recommendations filtered by mood
    Expected JSON: { "songs": [...], "mood": "happy|sad|energetic|chill" }
    """
    try:
        data = request.get_json()
        songs = data.get('songs', [])
        mood = data.get('mood', 'all')
        
        if not songs:
            return jsonify({'error': 'Songs array is required'}), 400
        
        # Generate mood-specific recommendations
        recommendations = gemini_engine.generate_mood_recommendations(songs, mood)
        
        return jsonify({
            'success': True,
            'mood': mood,
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        print(f"Error generating mood recommendations: {str(e)}")
        return jsonify({'error': f'Failed to generate mood recommendations: {str(e)}'}), 500

# Search for songs (for adding individual tracks)
@app.route('/api/search', methods=['GET'])
def search_songs():
    """
    Search for songs on Spotify
    Query params: ?q=song+name+artist
    """
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search Spotify
        results = spotify_service.search_tracks(query)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        print(f"Error searching songs: {str(e)}")
        return jsonify({'error': f'Failed to search songs: {str(e)}'}), 500

# Get song preview URL
@app.route('/api/preview/<track_id>', methods=['GET'])
def get_preview(track_id):
    """
    Get preview URL for a specific track
    """
    try:
        preview_url = spotify_service.get_track_preview(track_id)
        
        if not preview_url:
            return jsonify({'error': 'Preview not available for this track'}), 404
            
        return jsonify({
            'success': True,
            'previewUrl': preview_url
        }), 200
        
    except Exception as e:
        print(f"Error getting preview: {str(e)}")
        return jsonify({'error': f'Failed to get preview: {str(e)}'}), 500

# Calculate discovery stats
@app.route('/api/stats', methods=['POST'])
def calculate_stats():
    """
    Calculate discovery statistics
    Expected JSON: { "originalSongs": [...], "recommendations": [...] }
    """
    try:
        data = request.get_json()
        original_songs = data.get('originalSongs', [])
        recommendations = data.get('recommendations', [])
        
        # Calculate stats
        stats = gemini_engine.calculate_discovery_stats(original_songs, recommendations)
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        print(f"Error calculating stats: {str(e)}")
        return jsonify({'error': f'Failed to calculate stats: {str(e)}'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.route('/api/stored/imported', methods=['GET'])
def get_stored_imported_songs():
    """Get stored imported songs"""
    try:
        songs = ImportedSong.query.all()
        return jsonify({
            'success': True,
            'songs': [{
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'album': song.album,
                'genre': song.genre,
                'tempo': song.tempo,
                'mood': song.mood,
                'preview_url': song.preview_url
            } for song in songs]
        }), 200
    except Exception as e:
        print(f"Error fetching stored songs: {str(e)}")
        return jsonify({'error': f'Failed to fetch stored songs: {str(e)}'}), 500

@app.route('/api/stored/recommendations', methods=['GET'])
def get_stored_recommendations():
    """Get stored recommendations"""
    try:
        recommendations = Recommendation.query.all()
        return jsonify({
            'success': True,
            'recommendations': [{
                'id': rec.id,
                'title': rec.title,
                'artist': rec.artist,
                'album': rec.album,
                'genre': rec.genre,
                'tempo': rec.tempo,
                'mood': rec.mood,
                'reason': rec.reason,
                'preview_url': rec.preview_url
            } for rec in recommendations]
        }), 200
    except Exception as e:
        print(f"Error fetching stored recommendations: {str(e)}")
        return jsonify({'error': f'Failed to fetch stored recommendations: {str(e)}'}), 500

@app.route('/api/stored/playlist', methods=['GET', 'POST'])
def handle_built_playlist():
    """Get or update stored built playlist"""
    if request.method == 'GET':
        try:
            playlist_items = BuiltPlaylist.query.all()
            songs = []
            for item in playlist_items:
                rec = Recommendation.query.get(item.song_id)
                if rec:
                    songs.append({
                        'id': rec.id,
                        'title': rec.title,
                        'artist': rec.artist,
                        'album': rec.album,
                        'genre': rec.genre,
                        'tempo': rec.tempo,
                        'mood': rec.mood,
                        'reason': rec.reason,
                        'preview_url': rec.preview_url
                    })
            return jsonify({
                'success': True,
                'songs': songs
            }), 200
        except Exception as e:
            print(f"Error fetching built playlist: {str(e)}")
            return jsonify({'error': f'Failed to fetch built playlist: {str(e)}'}), 500
    else:  # POST
        try:
            data = request.get_json()
            songs = data.get('songs', [])
            
            # Clear existing playlist
            BuiltPlaylist.query.delete()
            
            # Add new songs
            for song in songs:
                playlist_item = BuiltPlaylist(
                    id=f"pl_{song['id']}",
                    song_id=song['id']
                )
                db.session.add(playlist_item)
            
            db.session.commit()
            return jsonify({'success': True}), 200
        except Exception as e:
            print(f"Error updating built playlist: {str(e)}")
            return jsonify({'error': f'Failed to update built playlist: {str(e)}'}), 500

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Create database tables before first request and ensure migrations for small schema changes
@app.before_request
def create_tables():
    # Create any missing tables
    db.create_all()

if __name__ == '__main__':
    # Check if required environment variables are set
    if not os.getenv('GEMINI_API_KEY'):
        print("âš ï¸  WARNING: GEMINI_API_KEY not found in .env file")
    
    if not os.getenv('SPOTIFY_CLIENT_ID') or not os.getenv('SPOTIFY_CLIENT_SECRET'):
        print("âš ï¸  WARNING: Spotify credentials not found in .env file")
    
    print("Music Recommendation Backend Starting...")
    print("Backend URL: http://localhost:5000")
    print("CORS enabled for React frontend")
    print("Connect your React app to: http://localhost:5000/api")
    
    # Run the Flask app
    app.run(debug=True)