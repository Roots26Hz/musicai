import React, { useState } from 'react';
import { Music, Plus, X, Play, ThumbsUp, Filter, TrendingUp, BarChart3, Users } from 'lucide-react';
import './App.css';

function App() {
  // State management
  const [activeTab, setActiveTab] = useState('import');
  const [playlistUrl, setPlaylistUrl] = useState('');
  const [importedSongs, setImportedSongs] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [builtPlaylist, setBuiltPlaylist] = useState([]);
  const [selectedFilters, setSelectedFilters] = useState({
    mood: 'all',
    genre: 'all',
    era: 'all'
  });

  // Mock data for demonstration (will be replaced with API calls)
  const mockImportedSongs = [
    { id: 1, title: 'Song Name 1', artist: 'Artist 1', genre: 'Pop', tempo: 120, mood: 'Happy' },
    { id: 2, title: 'Song Name 2', artist: 'Artist 2', genre: 'Rock', tempo: 140, mood: 'Energetic' },
    { id: 3, title: 'Song Name 3', artist: 'Artist 3', genre: 'Electronic', tempo: 128, mood: 'Chill' }
  ];

  const mockRecommendations = [
    { id: 101, title: 'Recommended Song 1', artist: 'New Artist 1', genre: 'Pop', reason: 'Similar tempo and mood to your favorites', previewUrl: '#' },
    { id: 102, title: 'Recommended Song 2', artist: 'New Artist 2', genre: 'Rock', reason: 'Popular among listeners with similar taste', previewUrl: '#' },
    { id: 103, title: 'Recommended Song 3', artist: 'New Artist 3', genre: 'Electronic', reason: 'Same genre and energy level', previewUrl: '#' }
  ];

  // Handlers
  const handleImportPlaylist = (e) => {
    e.preventDefault();
    // TODO: Connect to backend API
    setImportedSongs(mockImportedSongs);
    setActiveTab('imported');
  };

  const handleGenerateRecommendations = () => {
    // TODO: Connect to AI recommendation API
    setRecommendations(mockRecommendations);
    setActiveTab('recommendations');
  };

  const handleAddToPlaylist = (song) => {
    if (!builtPlaylist.find(s => s.id === song.id)) {
      setBuiltPlaylist([...builtPlaylist, song]);
    }
  };

  const handleRemoveFromPlaylist = (songId) => {
    setBuiltPlaylist(builtPlaylist.filter(s => s.id !== songId));
  };

  const handleFilterChange = (filterType, value) => {
    setSelectedFilters({ ...selectedFilters, [filterType]: value });
  };

  const handleExportPlaylist = (format) => {
    // TODO: Implement export functionality
    if (format === 'text') {
      const text = builtPlaylist.map(s => `${s.artist} - ${s.title}`).join('\n');
      navigator.clipboard.writeText(text);
      alert('Playlist copied to clipboard!');
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <Music size={32} />
            <h1>AI Music Recommender</h1>
          </div>
          <nav className="nav-tabs">
            <button 
              className={`nav-tab ${activeTab === 'import' ? 'active' : ''}`}
              onClick={() => setActiveTab('import')}
            >
              Import
            </button>
            <button 
              className={`nav-tab ${activeTab === 'imported' ? 'active' : ''}`}
              onClick={() => setActiveTab('imported')}
              disabled={importedSongs.length === 0}
            >
              Imported Songs ({importedSongs.length})
            </button>
            <button 
              className={`nav-tab ${activeTab === 'recommendations' ? 'active' : ''}`}
              onClick={() => setActiveTab('recommendations')}
              disabled={recommendations.length === 0}
            >
              Recommendations
            </button>
            <button 
              className={`nav-tab ${activeTab === 'playlist' ? 'active' : ''}`}
              onClick={() => setActiveTab('playlist')}
            >
              My Playlist ({builtPlaylist.length})
            </button>
            <button 
              className={`nav-tab ${activeTab === 'stats' ? 'active' : ''}`}
              onClick={() => setActiveTab('stats')}
            >
              Stats
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Import Tab */}
        {activeTab === 'import' && (
          <div className="tab-content">
            <div className="import-section">
              <h2>Import Your Playlist</h2>
              <p className="subtitle">Paste your Spotify or Apple Music playlist URL to get started</p>
              
              <form onSubmit={handleImportPlaylist} className="import-form">
                <input
                  type="text"
                  placeholder="https://music.apple.com/playlist/... or https://open.spotify.com/playlist/..."
                  value={playlistUrl}
                  onChange={(e) => setPlaylistUrl(e.target.value)}
                  className="url-input"
                />
                <button type="submit" className="btn-primary">
                  Import Playlist
                </button>
              </form>

              <div className="feature-cards">
                <div className="feature-card">
                  <Music size={24} />
                  <h3>Smart Import</h3>
                  <p>Automatically extracts metadata from your favorite playlists</p>
                </div>
                <div className="feature-card">
                  <TrendingUp size={24} />
                  <h3>AI Recommendations</h3>
                  <p>Get personalized suggestions based on your taste</p>
                </div>
                <div className="feature-card">
                  <BarChart3 size={24} />
                  <h3>Discover Stats</h3>
                  <p>Analyze your music preferences and trends</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Imported Songs Tab */}
        {activeTab === 'imported' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Imported Songs</h2>
              <button className="btn-primary" onClick={handleGenerateRecommendations}>
                Generate Recommendations
              </button>
            </div>
            
            <div className="songs-grid">
              {importedSongs.map(song => (
                <div key={song.id} className="song-card">
                  <div className="song-info">
                    <h3>{song.title}</h3>
                    <p>{song.artist}</p>
                    <div className="song-tags">
                      <span className="tag">{song.genre}</span>
                      <span className="tag">{song.mood}</span>
                      <span className="tag">{song.tempo} BPM</span>
                    </div>
                  </div>
                  <button 
                    className="btn-icon"
                    onClick={() => handleAddToPlaylist(song)}
                  >
                    <Plus size={20} />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations Tab */}
        {activeTab === 'recommendations' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>Personalized Recommendations</h2>
              <div className="filter-controls">
                <Filter size={20} />
                <select 
                  value={selectedFilters.mood}
                  onChange={(e) => handleFilterChange('mood', e.target.value)}
                  className="filter-select"
                >
                  <option value="all">All Moods</option>
                  <option value="happy">Happy</option>
                  <option value="sad">Sad</option>
                  <option value="energetic">Energetic</option>
                  <option value="chill">Chill</option>
                </select>
                <select 
                  value={selectedFilters.genre}
                  onChange={(e) => handleFilterChange('genre', e.target.value)}
                  className="filter-select"
                >
                  <option value="all">All Genres</option>
                  <option value="pop">Pop</option>
                  <option value="rock">Rock</option>
                  <option value="electronic">Electronic</option>
                  <option value="jazz">Jazz</option>
                </select>
              </div>
            </div>
            
            <div className="recommendations-feed">
              {mockRecommendations.map(song => (
                <div key={song.id} className="recommendation-card">
                  <div className="recommendation-content">
                    <div className="song-info">
                      <h3>{song.title}</h3>
                      <p>{song.artist}</p>
                      <div className="recommendation-reason">
                        <span className="reason-label">Why this song?</span>
                        <p>{song.reason}</p>
                      </div>
                    </div>
                    <div className="recommendation-actions">
                      <button className="btn-icon" title="Preview">
                        <Play size={20} />
                      </button>
                      <button className="btn-icon" title="Like">
                        <ThumbsUp size={20} />
                      </button>
                      <button 
                        className="btn-icon-primary"
                        onClick={() => handleAddToPlaylist(song)}
                      >
                        <Plus size={20} />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Playlist Builder Tab */}
        {activeTab === 'playlist' && (
          <div className="tab-content">
            <div className="section-header">
              <h2>My Playlist</h2>
              <div className="export-controls">
                <button 
                  className="btn-secondary"
                  onClick={() => handleExportPlaylist('text')}
                  disabled={builtPlaylist.length === 0}
                >
                  Copy as Text
                </button>
                <button 
                  className="btn-primary"
                  disabled={builtPlaylist.length === 0}
                >
                  Generate Share Link
                </button>
              </div>
            </div>
            
            {builtPlaylist.length === 0 ? (
              <div className="empty-state">
                <Music size={48} />
                <h3>Your playlist is empty</h3>
                <p>Add songs from your imported library or recommendations</p>
              </div>
            ) : (
              <div className="playlist-builder">
                {builtPlaylist.map((song, index) => (
                  <div key={song.id} className="playlist-item">
                    <span className="playlist-number">{index + 1}</span>
                    <div className="song-info">
                      <h3>{song.title}</h3>
                      <p>{song.artist}</p>
                    </div>
                    <button 
                      className="btn-icon-danger"
                      onClick={() => handleRemoveFromPlaylist(song.id)}
                    >
                      <X size={20} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Stats Tab */}
        {activeTab === 'stats' && (
          <div className="tab-content">
            <h2>Discovery Statistics</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <Users size={32} />
                <h3>New Artists</h3>
                <p className="stat-value">0%</p>
                <p className="stat-description">of recommendations</p>
              </div>
              <div className="stat-card">
                <BarChart3 size={32} />
                <h3>Genre Breakdown</h3>
                <p className="stat-description">Coming soon</p>
              </div>
              <div className="stat-card">
                <TrendingUp size={32} />
                <h3>Decade Distribution</h3>
                <p className="stat-description">Coming soon</p>
              </div>
            </div>
            <div className="info-message">
              Statistics will be available after importing playlists and generating recommendations
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;