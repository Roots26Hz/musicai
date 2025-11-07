import requests
import base64
from typing import List, Dict, Optional
import re

class SpotifyService:
    """
    Service for interacting with Spotify Web API
    """
    
    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize Spotify service with credentials
        
        Args:
            client_id: Spotify app client ID
            client_secret: Spotify app client secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1"
    
    def _get_access_token(self) -> Optional[str]:
        """
        Get access token for Spotify API using Client Credentials flow
        
        Returns:
            Access token string or None if failed
        """
        try:
            # Encode credentials
            auth_str = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_str.encode('utf-8')
            auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
            
            # Request token
            headers = {
                'Authorization': f'Basic {auth_base64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {'grant_type': 'client_credentials'}
            
            response = requests.post(self.token_url, headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                return self.access_token
            else:
                print(f"Failed to get access token: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting access token: {str(e)}")
            return None
    
    def _extract_playlist_id(self, playlist_url: str) -> Optional[str]:
        """
        Extract playlist ID from Spotify URL
        
        Args:
            playlist_url: Full Spotify playlist URL
            
        Returns:
            Playlist ID or None
        """
        try:
            # Pattern: https://open.spotify.com/playlist/{id}?...
            match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
            if match:
                return match.group(1)
            return None
        except Exception as e:
            print(f"Error extracting playlist ID: {str(e)}")
            return None
    
    def get_playlist_tracks(self, playlist_url: str) -> List[Dict]:
        """
        Fetch all tracks from a Spotify playlist
        
        Args:
            playlist_url: Full Spotify playlist URL
            
        Returns:
            List of song dictionaries with metadata
        """
        try:
            # Get access token
            if not self.access_token:
                self.access_token = self._get_access_token()
            
            if not self.access_token:
                print("Failed to authenticate with Spotify")
                return []
            
            # Extract playlist ID
            playlist_id = self._extract_playlist_id(playlist_url)
            if not playlist_id:
                print("Invalid playlist URL")
                return []
            
            # Fetch playlist tracks
            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f"{self.api_base_url}/playlists/{playlist_id}/tracks"
            
            songs = []
            offset = 0
            limit = 100
            
            while True:
                params = {'offset': offset, 'limit': limit}
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code != 200:
                    print(f"Error fetching tracks: {response.status_code}")
                    break
                
                data = response.json()
                items = data.get('items', [])
                
                if not items:
                    break
                
                # Extract song metadata
                for item in items:
                    track = item.get('track')
                    if not track:
                        continue
                    
                    song = self._extract_track_metadata(track)
                    if song:
                        songs.append(song)
                
                # Check if more tracks exist
                if len(items) < limit:
                    break
                
                offset += limit
            
            return songs
            
        except Exception as e:
            print(f"Error getting playlist tracks: {str(e)}")
            return []
    
    def _extract_track_metadata(self, track: Dict) -> Optional[Dict]:
        """
        Extract relevant metadata from Spotify track object
        
        Args:
            track: Spotify track object
            
        Returns:
            Simplified song dictionary
        """
        try:
            # Get audio features for tempo and energy
            track_id = track.get('id')
            audio_features = self._get_audio_features(track_id) if track_id else {}
            
            # Extract basic info
            song = {
                'id': track_id or f"track_{track.get('name', 'unknown')}",
                'title': track.get('name', 'Unknown Title'),
                'artist': ', '.join([artist['name'] for artist in track.get('artists', [])]),
                'genre': 'Unknown',  # Spotify doesn't provide genre in track object
                'tempo': int(audio_features.get('tempo', 120)),
                'mood': self._determine_mood(audio_features),
                'previewUrl': track.get('preview_url', '#'),
                'spotifyUrl': track.get('external_urls', {}).get('spotify', '#'),
                'albumArt': track.get('album', {}).get('images', [{}])[0].get('url', '')
            }
            
            return song
            
        except Exception as e:
            print(f"Error extracting track metadata: {str(e)}")
            return None
    
    def _get_audio_features(self, track_id: str) -> Dict:
        """
        Get audio features (tempo, energy, valence) for a track
        
        Args:
            track_id: Spotify track ID
            
        Returns:
            Audio features dictionary
        """
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f"{self.api_base_url}/audio-features/{track_id}"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            return {}
            
        except Exception as e:
            print(f"Error getting audio features: {str(e)}")
            return {}
    
    def _determine_mood(self, audio_features: Dict) -> str:
        """
        Determine mood based on audio features
        
        Args:
            audio_features: Spotify audio features
            
        Returns:
            Mood string (Happy/Sad/Energetic/Chill)
        """
        try:
            valence = audio_features.get('valence', 0.5)  # 0-1, happiness
            energy = audio_features.get('energy', 0.5)    # 0-1, intensity
            
            # Simple mood classification
            if valence > 0.6 and energy > 0.6:
                return 'Happy'
            elif valence < 0.4 and energy < 0.4:
                return 'Sad'
            elif energy > 0.7:
                return 'Energetic'
            else:
                return 'Chill'
                
        except Exception as e:
            print(f"Error determining mood: {str(e)}")
            return 'Neutral'
    
    def search_tracks(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for tracks on Spotify
        
        Args:
            query: Search query string
            limit: Number of results to return
            
        Returns:
            List of matching tracks
        """
        try:
            # Get access token if needed
            if not self.access_token:
                self.access_token = self._get_access_token()
            
            if not self.access_token:
                return []
            
            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f"{self.api_base_url}/search"
            params = {
                'q': query,
                'type': 'track',
                'limit': limit
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"Search failed: {response.status_code}")
                return []
            
            data = response.json()
            tracks = data.get('tracks', {}).get('items', [])
            
            results = []
            for track in tracks:
                song = self._extract_track_metadata(track)
                if song:
                    results.append(song)
            
            return results
            
        except Exception as e:
            print(f"Error searching tracks: {str(e)}")
            return []
    
    def get_track_preview(self, track_id: str) -> Optional[str]:
        """
        Get preview URL for a specific track
        
        Args:
            track_id: Spotify track ID
            
        Returns:
            Preview URL or None
        """
        try:
            if not self.access_token:
                self.access_token = self._get_access_token()
            
            if not self.access_token:
                return None
            
            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f"{self.api_base_url}/tracks/{track_id}"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                track = response.json()
                return track.get('preview_url')
            
            return None
            
        except Exception as e:
            print(f"Error getting track preview: {str(e)}")
            return None