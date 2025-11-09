from google import genai
from google.genai import types
import json
from typing import List, Dict

class GeminiRecommendationEngine:
    """
    AI-powered music recommendation engine using Google GenAI SDK
    Updated for google-genai (new unified SDK)
    """
    
    def __init__(self, api_key: str):
        """Initialize Gemini AI with API key using new SDK"""
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-pro'  # Using the stable Gemini Pro model
        
    def generate_recommendations(self, songs: List[Dict], count: int = 15) -> List[Dict]:
        """
        Generate personalized music recommendations based on playlist
        
        Args:
            songs: List of song dictionaries with metadata
            count: Number of recommendations to generate (default: 15)
            
        Returns:
            List of recommended songs with reasons
        """
        try:
            # Prepare context from imported songs
            song_context = self._prepare_song_context(songs)
            
            # Create prompt for Gemini
            prompt = f"""You are an expert music recommendation AI. Analyze this playlist and recommend {count} similar songs.

PLAYLIST ANALYSIS:
{song_context}

TASK:
Generate {count} song recommendations that match the musical taste shown in this playlist.

REQUIREMENTS:
1. Each recommendation should be a real song (not made up)
2. Consider: genre similarity, tempo, mood, artist connections, musical era
3. Provide a specific reason WHY each song fits this playlist
4. Include diverse recommendations (not all from same artist)
5. Format as JSON array

OUTPUT FORMAT (strict JSON):
[
  {{
    "id": "unique_id",
    "title": "Song Title",
    "artist": "Artist Name",
    "genre": "Genre",
    "tempo": 120,
    "mood": "Happy/Sad/Energetic/Chill",
    "reason": "Brief explanation why this song fits",
    "previewUrl": "#"
  }}
]

Return ONLY the JSON array, no additional text."""

            # Generate recommendations using new SDK
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            # Parse JSON response
            recommendations = self._parse_recommendations(response.text)
            
            return recommendations[:count]
            
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return []
    
    def generate_mood_recommendations(self, songs: List[Dict], mood: str, count: int = 10) -> List[Dict]:
        """
        Generate recommendations filtered by specific mood
        
        Args:
            songs: List of song dictionaries
            mood: Target mood (happy, sad, energetic, chill)
            count: Number of recommendations
            
        Returns:
            List of mood-filtered recommendations
        """
        try:
            song_context = self._prepare_song_context(songs)
            
            prompt = f"""You are an expert music recommendation AI. Based on this playlist, recommend {count} songs with a {mood.upper()} mood.

PLAYLIST CONTEXT:
{song_context}

TARGET MOOD: {mood.upper()}

REQUIREMENTS:
1. All recommendations must have {mood} mood/energy
2. Still maintain musical similarity to the playlist
3. Real songs only (verify they exist)
4. Explain why each song has this mood

OUTPUT FORMAT (strict JSON):
[
  {{
    "id": "unique_id",
    "title": "Song Title",
    "artist": "Artist Name",
    "genre": "Genre",
    "tempo": 120,
    "mood": "{mood.capitalize()}",
    "reason": "Why this song has {mood} mood and fits the playlist",
    "previewUrl": "#"
  }}
]

Return ONLY the JSON array."""

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            recommendations = self._parse_recommendations(response.text)
            
            return recommendations[:count]
            
        except Exception as e:
            print(f"Error generating mood recommendations: {str(e)}")
            return []
    
    def calculate_discovery_stats(self, original_songs: List[Dict], recommendations: List[Dict]) -> Dict:
        """
        Calculate discovery statistics comparing original playlist to recommendations
        
        Args:
            original_songs: Original playlist songs
            recommendations: AI-generated recommendations
            
        Returns:
            Dictionary with discovery statistics
        """
        try:
            # Extract unique artists
            original_artists = {song.get('artist', '') for song in original_songs}
            recommended_artists = {song.get('artist', '') for song in recommendations}
            new_artists = recommended_artists - original_artists
            
            # Calculate percentage of new artists
            new_artists_percentage = (len(new_artists) / len(recommended_artists) * 100) if recommended_artists else 0
            
            # Genre breakdown
            genre_counts = {}
            for song in recommendations:
                genre = song.get('genre', 'Unknown')
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
            # Mood breakdown
            mood_counts = {}
            for song in recommendations:
                mood = song.get('mood', 'Unknown')
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            # Tempo analysis
            tempos = [song.get('tempo', 0) for song in recommendations if song.get('tempo')]
            avg_tempo = sum(tempos) / len(tempos) if tempos else 0
            
            return {
                'newArtistsPercentage': round(new_artists_percentage, 1),
                'newArtistsCount': len(new_artists),
                'totalRecommendedArtists': len(recommended_artists),
                'genreBreakdown': genre_counts,
                'moodBreakdown': mood_counts,
                'averageTempo': round(avg_tempo),
                'totalRecommendations': len(recommendations)
            }
            
        except Exception as e:
            print(f"Error calculating stats: {str(e)}")
            return {}
    
    def _prepare_song_context(self, songs: List[Dict]) -> str:
        """
        Prepare detailed song context for AI prompt
        """
        context = ["PLAYLIST ANALYSIS:"]
        
        # Collect unique genres and moods
        genres = {}
        moods = {}
        total_tempo = 0
        valid_songs = 0
        
        # First pass - collect statistics
        for song in songs[:20]:  # Limit to first 20 songs for analysis
            if not isinstance(song, dict):
                continue
                
            genre = song.get('genre', 'Unknown')
            mood = song.get('mood', 'Unknown')
            tempo = song.get('tempo', 0)
            
            genres[genre] = genres.get(genre, 0) + 1
            moods[mood] = moods.get(mood, 0) + 1
            
            if tempo > 0:
                total_tempo += tempo
                valid_songs += 1
        
        # Add summary statistics
        avg_tempo = round(total_tempo / valid_songs) if valid_songs > 0 else 0
        context.append("\nPlaylist Overview:")
        context.append(f"- Dominant Genres: {', '.join(sorted(genres, key=genres.get, reverse=True)[:3])}")
        context.append(f"- Common Moods: {', '.join(sorted(moods, key=moods.get, reverse=True)[:3])}")
        context.append(f"- Average Tempo: {avg_tempo} BPM")
        
        # Add individual songs
        context.append("\nSong Details:")
        for i, song in enumerate(songs[:20], 1):
            if not isinstance(song, dict):
                continue
                
            title = song.get('title', 'Unknown')
            artist = song.get('artist', 'Unknown')
            genre = song.get('genre', 'Unknown')
            tempo = song.get('tempo', 'Unknown')
            mood = song.get('mood', 'Unknown')
            popularity = song.get('popularity', 0)
            energy = song.get('energy', 0.5)
            
            context.append(
                f"{i}. {title} by {artist}\n"
                f"   Genre: {genre} | Tempo: {tempo} BPM | Mood: {mood}\n"
                f"   Popularity: {popularity}/100 | Energy: {round(energy * 100)}%"
            )
        
        return "\n".join(context)
    
    def _parse_recommendations(self, response_text: str) -> List[Dict]:
        """
        Parse and validate JSON recommendations from Gemini response
        """
        try:
            # Extract JSON array from response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                print("No JSON array found in response")
                return []
            
            json_str = response_text[start_idx:end_idx]
            
            # Clean up potential formatting issues
            json_str = json_str.replace('\n', ' ').replace('\r', '')
            json_str = ' '.join(json_str.split())  # Normalize whitespace
            
            recommendations = json.loads(json_str)
            
            if not isinstance(recommendations, list):
                print("Response is not a list")
                return []
            
            # Validate and normalize each recommendation
            validated_recommendations = []
            for i, rec in enumerate(recommendations):
                if not isinstance(rec, dict):
                    continue
                    
                # Required fields check
                if not all(rec.get(key) for key in ['title', 'artist']):
                    continue
                
                # Normalize and validate fields
                normalized_rec = {
                    'id': rec.get('id', f"rec_{i}"),
                    'title': str(rec['title']).strip(),
                    'artist': str(rec['artist']).strip(),
                    'genre': str(rec.get('genre', 'Unknown')).strip(),
                    'tempo': self._validate_tempo(rec.get('tempo', 120)),
                    'mood': self._validate_mood(rec.get('mood', 'Neutral')),
                    'reason': str(rec.get('reason', 'Recommended based on playlist similarity')).strip(),
                    'previewUrl': rec.get('previewUrl', '#'),
                    'confidence': float(rec.get('confidence', 0.8)),  # AI confidence in recommendation
                    'matchScore': float(rec.get('matchScore', 0.7)),  # How well it matches playlist
                }
                
                # Additional validation
                if len(normalized_rec['title']) < 1 or len(normalized_rec['artist']) < 1:
                    continue
                    
                validated_recommendations.append(normalized_rec)
            
            # Sort by match score if available
            validated_recommendations.sort(key=lambda x: x['matchScore'], reverse=True)
            
            return validated_recommendations
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print(f"Response text: {response_text[:500]}")
            return []
        except Exception as e:
            print(f"Error parsing recommendations: {str(e)}")
            return []
            
    def _validate_tempo(self, tempo) -> int:
        """Validate and normalize tempo value"""
        try:
            tempo = int(float(tempo))
            return max(min(tempo, 300), 40)  # Clamp between 40-300 BPM
        except (ValueError, TypeError):
            return 120
            
    def _validate_mood(self, mood: str) -> str:
        """Validate and normalize mood value"""
        valid_moods = {'Happy', 'Sad', 'Energetic', 'Chill', 'Neutral'}
        mood = str(mood).strip().title()
        return mood if mood in valid_moods else 'Neutral'