/**
 * API Service - Handles all HTTP requests to the backend
 */

import { API_BASE_URL, API_ENDPOINTS } from '@/config/api';

// Re-export types from mockBackend for compatibility
export interface User {
  id: string;
  username: string;
  email: string;
  createdAt?: string;
}

export interface LeaderboardEntry {
  id: string;
  userId?: string;
  username: string;
  score: number;
  mode: "walls" | "pass-through";
  timestamp: number; // Will convert from ISO string
}

export interface ActivePlayer {
  id: string;
  username: string;
  score: number;
  mode: "walls" | "pass-through";
  snake: { x: number; y: number }[];
  food: { x: number; y: number };
  isGameOver: boolean;
  direction?: "UP" | "DOWN" | "LEFT" | "RIGHT";
  startedAt?: string;
}

// API Error type
export interface ApiError {
  error: string;
  message: string;
  code?: number;
  details?: Array<{ field: string; message: string }>;
}

// Token management
const TOKEN_KEY = 'authToken';
const USER_KEY = 'currentUser';

export const tokenManager = {
  getToken: (): string | null => {
    return localStorage.getItem(TOKEN_KEY);
  },
  
  setToken: (token: string): void => {
    localStorage.setItem(TOKEN_KEY, token);
  },
  
  removeToken: (): void => {
    localStorage.removeItem(TOKEN_KEY);
  },
  
  getUser: (): User | null => {
    const userData = localStorage.getItem(USER_KEY);
    return userData ? JSON.parse(userData) : null;
  },
  
  setUser: (user: User): void => {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },
  
  removeUser: (): void => {
    localStorage.removeItem(USER_KEY);
  },
  
  clearAuth: (): void => {
    tokenManager.removeToken();
    tokenManager.removeUser();
  },
};

// HTTP client with auth header injection
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = tokenManager.getToken();
  
  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
  };

  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, config);
    
    // Handle 401 - clear auth and throw
    if (response.status === 401) {
      tokenManager.clearAuth();
      const error: ApiError = await response.json().catch(() => ({
        error: 'Unauthorized',
        message: 'Authentication required',
        code: 401,
      }));
      throw error;
    }
    
    // Handle other error status codes
    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        error: 'RequestFailed',
        message: `Request failed with status ${response.status}`,
        code: response.status,
      }));
      throw error;
    }
    
    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }
    
    return await response.json();
  } catch (error) {
    // Re-throw ApiError
    if ((error as ApiError).error) {
      throw error;
    }
    
    // Network or other errors
    throw {
      error: 'NetworkError',
      message: error instanceof Error ? error.message : 'Network request failed',
    } as ApiError;
  }
}

// Helper to convert ISO timestamp to milliseconds
function parseTimestamp(isoString: string): number {
  return new Date(isoString).getTime();
}

// Auth API
export const authAPI = {
  login: async (email: string, password: string): Promise<{ user: User; token: string; error?: string }> => {
    try {
      const response = await apiRequest<{ user: User; token: string }>(
        API_ENDPOINTS.LOGIN,
        {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        }
      );
      
      // Store token and user
      tokenManager.setToken(response.token);
      tokenManager.setUser(response.user);
      
      return response;
    } catch (error) {
      const apiError = error as ApiError;
      return {
        user: null as any,
        token: '',
        error: apiError.message || 'Login failed',
      };
    }
  },

  signup: async (username: string, email: string, password: string): Promise<{ user: User; token: string; error?: string }> => {
    try {
      const response = await apiRequest<{ user: User; token: string }>(
        API_ENDPOINTS.SIGNUP,
        {
          method: 'POST',
          body: JSON.stringify({ username, email, password }),
        }
      );
      
      // Store token and user
      tokenManager.setToken(response.token);
      tokenManager.setUser(response.user);
      
      return response;
    } catch (error) {
      const apiError = error as ApiError;
      return {
        user: null as any,
        token: '',
        error: apiError.message || 'Signup failed',
      };
    }
  },

  logout: async (): Promise<void> => {
    try {
      await apiRequest(API_ENDPOINTS.LOGOUT, { method: 'POST' });
    } catch (error) {
      // Ignore logout errors, still clear local auth
      console.error('Logout error:', error);
    } finally {
      tokenManager.clearAuth();
    }
  },

  getCurrentUser: (): User | null => {
    return tokenManager.getUser();
  },
  
  // Validate token by fetching current user from backend
  validateToken: async (): Promise<User | null> => {
    try {
      const user = await apiRequest<User>(API_ENDPOINTS.ME);
      tokenManager.setUser(user);
      return user;
    } catch (error) {
      tokenManager.clearAuth();
      return null;
    }
  },
};

// Leaderboard API
export const leaderboardAPI = {
  getLeaderboard: async (params?: {
    mode?: "walls" | "pass-through";
    limit?: number;
    offset?: number;
  }): Promise<LeaderboardEntry[]> => {
    const queryParams = new URLSearchParams();
    if (params?.mode) queryParams.append('mode', params.mode);
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());
    
    const query = queryParams.toString();
    const endpoint = query ? `${API_ENDPOINTS.LEADERBOARD}?${query}` : API_ENDPOINTS.LEADERBOARD;
    
    const response = await apiRequest<{
      entries: Array<Omit<LeaderboardEntry, 'timestamp'> & { timestamp: string }>;
      total: number;
      limit: number;
      offset: number;
    }>(endpoint);
    
    // Convert timestamps from ISO strings to numbers
    return response.entries.map(entry => ({
      ...entry,
      timestamp: parseTimestamp(entry.timestamp),
    }));
  },

  submitScore: async (score: number, mode: "walls" | "pass-through"): Promise<void> => {
    await apiRequest<LeaderboardEntry>(API_ENDPOINTS.LEADERBOARD_SCORES, {
      method: 'POST',
      body: JSON.stringify({ score, mode }),
    });
  },

  getTopScores: async (limit: number = 10, mode?: "walls" | "pass-through"): Promise<LeaderboardEntry[]> => {
    const queryParams = new URLSearchParams();
    queryParams.append('limit', limit.toString());
    if (mode) queryParams.append('mode', mode);
    
    const endpoint = `${API_ENDPOINTS.LEADERBOARD_TOP}?${queryParams.toString()}`;
    
    const entries = await apiRequest<Array<Omit<LeaderboardEntry, 'timestamp'> & { timestamp: string }>>(
      endpoint
    );
    
    // Convert timestamps from ISO strings to numbers
    return entries.map(entry => ({
      ...entry,
      timestamp: parseTimestamp(entry.timestamp),
    }));
  },
  
  getUserScores: async (userId: string, mode?: "walls" | "pass-through"): Promise<LeaderboardEntry[]> => {
    const queryParams = new URLSearchParams();
    if (mode) queryParams.append('mode', mode);
    
    const query = queryParams.toString();
    const endpoint = query 
      ? `${API_ENDPOINTS.LEADERBOARD_USER(userId)}?${query}`
      : API_ENDPOINTS.LEADERBOARD_USER(userId);
    
    const entries = await apiRequest<Array<Omit<LeaderboardEntry, 'timestamp'> & { timestamp: string }>>(
      endpoint
    );
    
    return entries.map(entry => ({
      ...entry,
      timestamp: parseTimestamp(entry.timestamp),
    }));
  },
};

// Spectate API
export const spectateAPI = {
  getActivePlayers: async (mode?: "walls" | "pass-through"): Promise<ActivePlayer[]> => {
    const queryParams = new URLSearchParams();
    if (mode) queryParams.append('mode', mode);
    
    const query = queryParams.toString();
    const endpoint = query ? `${API_ENDPOINTS.SPECTATE_PLAYERS}?${query}` : API_ENDPOINTS.SPECTATE_PLAYERS;
    
    return await apiRequest<ActivePlayer[]>(endpoint);
  },

  watchPlayer: async (playerId: string): Promise<ActivePlayer | null> => {
    try {
      return await apiRequest<ActivePlayer>(API_ENDPOINTS.SPECTATE_PLAYER(playerId));
    } catch (error) {
      const apiError = error as ApiError;
      if (apiError.code === 404) {
        return null;
      }
      throw error;
    }
  },
};

// Export for backward compatibility with mockBackend
export const mockAuth = authAPI;
export const mockLeaderboardAPI = leaderboardAPI;
export const mockSpectateAPI = spectateAPI;
