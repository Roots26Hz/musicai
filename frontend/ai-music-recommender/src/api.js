const API_BASE_URL = 'http://127.0.0.1:5000/api';

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

export const calculateStats = async (originalSongs, recommendations) => {
  const response = await fetch(`${API_BASE_URL}/stats`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ originalSongs, recommendations }),
  });
  return response.json();
};

export const fetchStoredImportedSongs = async () => {
  const response = await fetch(`${API_BASE_URL}/stored/imported`);
  return response.json();
};

export const fetchStoredRecommendations = async () => {
  const response = await fetch(`${API_BASE_URL}/stored/recommendations`);
  return response.json();
};

export const fetchStoredPlaylist = async () => {
  const response = await fetch(`${API_BASE_URL}/stored/playlist`);
  return response.json();
};