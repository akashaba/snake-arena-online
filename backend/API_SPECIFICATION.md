# Neon Snake Arena - API Specification

## Overview

This document describes the backend API requirements for the Neon Snake Arena Online game, derived from frontend implementation analysis.

## Base URL

- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://api.snake-arena.com/api/v1`

## Authentication

The API uses JWT (JSON Web Token) based authentication. After successful login or signup, clients receive a token that must be included in subsequent requests.

**Authorization Header Format:**
```
Authorization: Bearer <your-jwt-token>
```

## API Endpoints

### 1. Authentication

#### POST `/auth/login`
Authenticate a user with email and password.

**Request Body:**
```json
{
  "email": "player@example.com",
  "password": "password123"
}
```

**Success Response (200):**
```json
{
  "user": {
    "id": "abc123def456",
    "username": "NeonMaster",
    "email": "player@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (401):**
```json
{
  "error": "InvalidCredentials",
  "message": "Invalid email or password"
}
```

#### POST `/auth/signup`
Create a new user account.

**Request Body:**
```json
{
  "username": "NeonMaster",
  "email": "player@example.com",
  "password": "password123"
}
```

**Success Response (201):**
```json
{
  "user": {
    "id": "abc123def456",
    "username": "NeonMaster",
    "email": "player@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (409):**
```json
{
  "error": "UserExists",
  "message": "User already exists"
}
```

#### POST `/auth/logout`
Invalidate the current user session (requires authentication).

**Success Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

#### GET `/auth/me`
Get currently authenticated user information (requires authentication).

**Success Response (200):**
```json
{
  "id": "abc123def456",
  "username": "NeonMaster",
  "email": "player@example.com",
  "createdAt": "2023-12-01T10:30:00Z"
}
```

### 2. Leaderboard

#### GET `/leaderboard`
Get the full leaderboard with optional filtering and pagination.

**Query Parameters:**
- `mode` (optional): Filter by game mode (`walls` or `pass-through`)
- `limit` (optional): Maximum entries to return (default: 20, max: 100)
- `offset` (optional): Number of entries to skip (default: 0)

**Success Response (200):**
```json
{
  "entries": [
    {
      "id": "entry123",
      "userId": "abc123",
      "username": "NeonMaster",
      "score": 850,
      "mode": "walls",
      "timestamp": "2023-12-01T14:30:00Z"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

#### GET `/leaderboard/top`
Get top N scores from the leaderboard.

**Query Parameters:**
- `limit` (optional): Number of top scores (default: 10, max: 100)
- `mode` (optional): Filter by game mode (`walls` or `pass-through`)

**Success Response (200):**
```json
[
  {
    "id": "entry123",
    "userId": "abc123",
    "username": "NeonMaster",
    "score": 850,
    "mode": "walls",
    "timestamp": "2023-12-01T14:30:00Z"
  }
]
```

#### POST `/leaderboard/scores`
Submit a new score (requires authentication).

**Request Body:**
```json
{
  "score": 850,
  "mode": "walls"
}
```

**Success Response (201):**
```json
{
  "id": "entry123",
  "userId": "abc123",
  "username": "NeonMaster",
  "score": 850,
  "mode": "walls",
  "timestamp": "2023-12-01T14:30:00Z"
}
```

#### GET `/leaderboard/user/{userId}`
Get all scores for a specific user.

**Query Parameters:**
- `mode` (optional): Filter by game mode

**Success Response (200):**
```json
[
  {
    "id": "entry123",
    "userId": "abc123",
    "username": "NeonMaster",
    "score": 850,
    "mode": "walls",
    "timestamp": "2023-12-01T14:30:00Z"
  }
]
```

### 3. Spectate

#### GET `/spectate/players`
Get all currently active players.

**Query Parameters:**
- `mode` (optional): Filter by game mode

**Success Response (200):**
```json
[
  {
    "id": "player123",
    "username": "NeonMaster",
    "score": 230,
    "mode": "walls",
    "snake": [
      { "x": 10, "y": 10 },
      { "x": 9, "y": 10 },
      { "x": 8, "y": 10 }
    ],
    "food": { "x": 15, "y": 5 },
    "isGameOver": false,
    "direction": "RIGHT",
    "startedAt": "2023-12-01T15:00:00Z"
  }
]
```

#### GET `/spectate/players/{playerId}`
Get detailed game state for a specific player.

**Success Response (200):**
```json
{
  "id": "player123",
  "username": "NeonMaster",
  "score": 230,
  "mode": "walls",
  "snake": [
    { "x": 10, "y": 10 },
    { "x": 9, "y": 10 },
    { "x": 8, "y": 10 }
  ],
  "food": { "x": 15, "y": 5 },
  "isGameOver": false,
  "direction": "RIGHT",
  "startedAt": "2023-12-01T15:00:00Z"
}
```

### 4. User Profile

#### GET `/users/{userId}`
Get public profile information for a user.

**Success Response (200):**
```json
{
  "id": "abc123",
  "username": "NeonMaster",
  "createdAt": "2023-12-01T10:30:00Z",
  "totalGames": 150,
  "highestScore": 850,
  "favoriteMode": "walls"
}
```

#### GET `/users/{userId}/stats`
Get detailed statistics for a user.

**Success Response (200):**
```json
{
  "totalGames": 150,
  "totalScore": 12500,
  "averageScore": 83.33,
  "highestScore": 850,
  "wallModeGames": 90,
  "passThroughModeGames": 60,
  "bestWallScore": 850,
  "bestPassThroughScore": 720,
  "rank": 5
}
```

## Data Models

### User
```typescript
{
  id: string;
  username: string;
  email: string;
  createdAt?: string; // ISO 8601 datetime
}
```

### LeaderboardEntry
```typescript
{
  id: string;
  userId: string;
  username: string;
  score: number;
  mode: "walls" | "pass-through";
  timestamp: string; // ISO 8601 datetime
}
```

### Position
```typescript
{
  x: number; // 0-19 (grid is 20x20)
  y: number; // 0-19
}
```

### ActivePlayer
```typescript
{
  id: string;
  username: string;
  score: number;
  mode: "walls" | "pass-through";
  snake: Position[]; // Head is first element
  food: Position;
  isGameOver: boolean;
  direction?: "UP" | "DOWN" | "LEFT" | "RIGHT";
  startedAt?: string; // ISO 8601 datetime
}
```

## Business Rules

### Authentication
1. Username must be 3-30 characters, alphanumeric with underscores and hyphens only
2. Password must be at least 6 characters
3. Email must be unique
4. JWT tokens should have reasonable expiration (e.g., 24 hours)

### Game Rules
1. Grid size is 20x20 (positions from 0-19 for both x and y)
2. Two game modes:
   - **walls**: Snake dies when hitting walls or itself
   - **pass-through**: Snake wraps around edges, only dies when hitting itself
3. Each food eaten increases score by 10 points
4. Snake starts with 3 segments

### Leaderboard
1. Scores are submitted when game ends
2. Users can have multiple entries on leaderboard
3. Entries are sorted by score (highest first)
4. Timestamp is used for tie-breaking
5. Mode filtering allows separate leaderboards for different game modes

### Spectate
1. Only show active (currently playing) games
2. Update game state periodically (frontend polls every 2 seconds)
3. Players disappear from active list when game ends
4. Game state includes full snake positions and food location

## Error Handling

All errors follow this format:

```json
{
  "error": "ErrorType",
  "message": "Human-readable error message",
  "code": 400
}
```

**Common Error Codes:**
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (authentication required or invalid)
- `404` - Not Found (resource doesn't exist)
- `409` - Conflict (e.g., user already exists)
- `422` - Unprocessable Entity (validation failed)
- `500` - Internal Server Error

## Rate Limiting

Consider implementing rate limiting for:
- Login attempts: 5 per minute per IP
- Signup: 3 per hour per IP
- Score submission: 10 per minute per user
- Leaderboard queries: 60 per minute per IP

## CORS Configuration

The backend should allow CORS requests from the frontend domain with credentials.

## Future Enhancements (Optional)

1. **WebSocket Support**: Real-time game state updates for spectators
2. **Multiplayer**: Allow multiple snakes in same arena
3. **Replays**: Store and retrieve game replays
4. **Achievements**: Track and award achievements
5. **Friends System**: Add/follow other players
6. **Chat**: In-game messaging
7. **Tournaments**: Organized competitive events
8. **Power-ups**: Special items with temporary effects

## Implementation Notes

1. The frontend currently uses localStorage for persisting auth state
2. Score submission happens automatically when game ends (if authenticated)
3. The frontend polls the spectate endpoint every 2 seconds
4. Consider implementing WebSocket for real-time spectate updates in future
5. Grid size is hardcoded to 20x20 in the game engine
