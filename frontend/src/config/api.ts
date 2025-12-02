/**
 * API Configuration
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login',
  SIGNUP: '/auth/signup',
  LOGOUT: '/auth/logout',
  ME: '/auth/me',
  
  // Leaderboard
  LEADERBOARD: '/leaderboard',
  LEADERBOARD_TOP: '/leaderboard/top',
  LEADERBOARD_SCORES: '/leaderboard/scores',
  LEADERBOARD_USER: (userId: string) => `/leaderboard/user/${userId}`,
  
  // Spectate
  SPECTATE_PLAYERS: '/spectate/players',
  SPECTATE_PLAYER: (playerId: string) => `/spectate/players/${playerId}`,
  
  // Users
  USER_PROFILE: (userId: string) => `/users/${userId}`,
  USER_STATS: (userId: string) => `/users/${userId}/stats`,
} as const;
