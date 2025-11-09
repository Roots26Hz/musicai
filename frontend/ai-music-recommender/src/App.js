import React, { useState, useEffect } from 'react';
import { Music, Plus, X, Play, ThumbsUp, Filter, TrendingUp, BarChart3, Users } from 'lucide-react';
import './App.css';
import { importPlaylist, generateRecommendations, calculateStats, fetchStoredImportedSongs, fetchStoredRecommendations, fetchStoredPlaylist } from './api';

function App() {
  // State management
  const [activeTab, setActiveTab] = useState('import');
  const [playlistUrl, setPlaylistUrl] = useState('');
  const [importedSongs, setImportedSongs] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [builtPlaylist, setBuiltPlaylist] = useState([]);
  const [isImporting, setIsImporting] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isCalculatingStats, setIsCalculatingStats] = useState(false);
  const [stats, setStats] = useState(null);
  const [selectedFilters, setSelectedFilters] = useState({
    mood: 'all',
    genre: 'all',
    era: 'all'
  });

  // Using actual data from API

  // Handlers
const handleImportPlaylist = async (e) => {
  e.preventDefault();
  setIsImporting(true);
  try {
    const data = await importPlaylist(playlistUrl);
    setImportedSongs(data.songs || []);
    setActiveTab('imported');
  } catch (error) {
    console.error('Error importing playlist:', error);
    alert('Failed to import playlist. Make sure backend is running.');
  } finally {
    setIsImporting(false);
  }
};

const handleGenerateRecommendations = async () => {
  setIsGenerating(true);
  try {
    const data = await generateRecommendations(importedSongs);
    setRecommendations(data.recommendations || []);
    setActiveTab('recommendations');
  } catch (error) {
    console.error('Error generating recommendations:', error);
    alert('Failed to generate recommendations.');
  } finally {
    setIsGenerating(false);
  }
};

// Calculate statistics by calling backend /api/stats
const handleCalculateStats = async () => {
  // If there are no recommendations or no imported songs, clear stats
  if (!recommendations || recommendations.length === 0) {
    setStats(null);
    return;
  }

  setIsCalculatingStats(true);
  try {
    const res = await calculateStats(importedSongs, recommendations);
    // backend returns { success: True, stats: { ... } }
    setStats(res.stats || null);
  } catch (err) {
    console.error('Error calculating stats:', err);
    setStats(null);
  } finally {
    setIsCalculatingStats(false);
  }
};

  // Load stored data when app starts
  useEffect(() => {
    const loadStoredData = async () => {
      try {
        // Fetch all stored data in parallel
        const [importedData, recommendationsData, playlistData] = await Promise.all([
          fetchStoredImportedSongs(),
          fetchStoredRecommendations(),
          fetchStoredPlaylist()
        ]);

        if (importedData.success) {
          setImportedSongs(importedData.songs);
        }
        if (recommendationsData.success) {
          setRecommendations(recommendationsData.recommendations);
        }
        if (playlistData.success) {
          setBuiltPlaylist(playlistData.songs);
        }
      } catch (error) {
        console.error('Error loading stored data:', error);
      }
    };

    loadStoredData();
  }, []);

  useEffect(() => {
    // Auto-calc stats when user navigates to Stats tab and recommendations exist
    if (activeTab === 'stats') {
      handleCalculateStats();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab, recommendations]);  const savePlaylistToServer = async (updatedPlaylist) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/stored/playlist', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ songs: updatedPlaylist }),
      });
      if (!response.ok) {
        console.error('Failed to save playlist to server');
      }
    } catch (error) {
      console.error('Error saving playlist:', error);
    }
  };

  const handleAddToPlaylist = (song) => {
    if (!builtPlaylist.find(s => s.id === song.id)) {
      const updatedPlaylist = [...builtPlaylist, song];
      setBuiltPlaylist(updatedPlaylist);
      savePlaylistToServer(updatedPlaylist);
    }
  };

  const handleRemoveFromPlaylist = (songId) => {
    const updatedPlaylist = builtPlaylist.filter(s => s.id !== songId);
    setBuiltPlaylist(updatedPlaylist);
    savePlaylistToServer(updatedPlaylist);
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
            <h1>musicai - An AI Music Recommender</h1>
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
        {(isImporting || isGenerating) && (
          <div className="loading-overlay" role="status" aria-live="polite">
            <div className="loading-box">
              <div className="spinner" />
              <div className="loading-text">{isImporting ? 'Importing playlist...' : 'Generating recommendations...'}</div>
            </div>
          </div>
        )}
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
                <button type="submit" className="btn-primary" disabled={isImporting}>
                  {isImporting ? 'Importing...' : 'Import Playlist'}
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
              <button className="btn-primary" onClick={handleGenerateRecommendations} disabled={isGenerating || importedSongs.length === 0}>
                {isGenerating ? 'Generating...' : 'Generate Recommendations'}
              </button>
            </div>
            
            <div className="songs-grid">
              {importedSongs.map(song => (
                <div key={song.id} className="song-card">
                  <div className="song-info">
                    <h3>{song.title}</h3>
                    <p>{song.artist}</p>
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
            </div>
            
            <div className="recommendations-feed">
              {recommendations.length === 0 && !isGenerating ? (
                <div className="empty-state">
                  <h3>No recommendations yet</h3>
                  <p>Click Generate Recommendations in the Imported Songs tab to fetch recommendations.</p>
                </div>
              ) : (
                recommendations.map(song => (
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
                ))
              )}
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
            <div style={{ marginBottom: '12px' }}>
              <button className="btn-secondary" onClick={handleCalculateStats} disabled={isCalculatingStats || recommendations.length === 0}>
                {isCalculatingStats ? 'Calculating...' : 'Refresh Stats'}
              </button>
            </div>
            <div className="stats-grid">
              <div className="stat-card">
                <Users size={32} />
                <h3>New Artists</h3>
                <p className="stat-value">{stats ? `${stats.newArtistsPercentage ?? 0}%` : '--'}</p>
                <p className="stat-description">{stats ? `${stats.newArtistsCount ?? 0} new artists` : 'Stats unavailable'}</p>
              </div>

              <div className="stat-card">
                <BarChart3 size={32} />
                <h3>Average Tempo</h3>
                <p className="stat-value">{stats ? `${stats.averageTempo ?? 0} BPM` : '--'}</p>
                <p className="stat-description">Based on recommendations</p>
              </div>

              <div className="stat-card">
                <TrendingUp size={32} />
                <h3>Total Recommendations</h3>
                <p className="stat-value">{stats ? `${stats.totalRecommendations ?? recommendations.length}` : '--'}</p>
                <p className="stat-description">Recommendations analyzed</p>
              </div>
            </div>

            <div style={{ marginTop: '16px' }}>
              <h3>Mood Breakdown</h3>
              {stats && stats.moodBreakdown ? (
                <div style={{ display: 'flex', gap: '12px', marginTop: '8px', flexWrap: 'wrap' }}>
                  {Object.entries(stats.moodBreakdown).map(([mood, count]) => (
                    <div key={mood} className="stat-card" style={{ padding: '12px 16px' }}>
                      <strong>{mood}</strong>
                      <div style={{ marginTop: '6px' }}>{count} songs</div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="stat-description">Mood breakdown will appear here after stats are calculated.</p>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;