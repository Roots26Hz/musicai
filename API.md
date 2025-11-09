# MusicAI API Documentation

This document details the endpoints available in the MusicAI backend API.

## Base URL

All endpoints are prefixed with: `http://localhost:5000/api`

## Authentication

Currently, authentication is handled through environment variables for Spotify and Gemini AI credentials.

## Endpoints

### Import Playlist

```http
POST /import
```

Import a playlist from Spotify.

**Request Body:**
```json
{
  "playlistUrl": "https://open.spotify.com/playlist/..."
}
```

**Response:**
```json
{
  "success": true,
  "platform": "spotify",
  "songs": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "album": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string",
      "preview_url": "string"
    }
  ],
  "count": "number"
}
```

### Generate Recommendations

```http
POST /recommend
```

Generate AI-powered recommendations based on imported songs.

**Request Body:**
```json
{
  "songs": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "album": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string",
      "reason": "string",
      "preview_url": "string"
    }
  ],
  "count": "number"
}
```

### Get Stored Imported Songs

```http
GET /stored/imported
```

Retrieve previously imported songs from the database.

**Response:**
```json
{
  "success": true,
  "songs": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "album": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string",
      "preview_url": "string"
    }
  ]
}
```

### Get Stored Recommendations

```http
GET /stored/recommendations
```

Retrieve previously generated recommendations from the database.

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "album": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string",
      "reason": "string",
      "preview_url": "string"
    }
  ]
}
```

### Manage Built Playlist

```http
GET /stored/playlist
```

Retrieve the user's built playlist.

**Response:**
```json
{
  "success": true,
  "songs": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "album": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string",
      "reason": "string",
      "preview_url": "string"
    }
  ]
}
```

```http
POST /stored/playlist
```

Update the user's built playlist.

**Request Body:**
```json
{
  "songs": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "album": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string",
      "preview_url": "string"
    }
  ]
}
```

**Response:**
```json
{
  "success": true
}
```

### Calculate Statistics

```http
POST /stats
```

Calculate discovery statistics based on original songs and recommendations.

**Request Body:**
```json
{
  "originalSongs": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string"
    }
  ],
  "recommendations": [
    {
      "id": "string",
      "title": "string",
      "artist": "string",
      "genre": "string",
      "tempo": "number",
      "mood": "string"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "newArtistsPercentage": "number",
    "newArtistsCount": "number",
    "averageTempo": "number",
    "totalRecommendations": "number",
    "moodBreakdown": {
      "happy": "number",
      "energetic": "number",
      "calm": "number",
      "melancholic": "number"
    }
  }
}
```

## Error Responses

All endpoints can return the following error responses:

```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

Currently, there are no rate limits implemented on the API endpoints.

(Spotify and Gemini API rate limits are user-dependant on the plan they use and the model which is used for API calling)