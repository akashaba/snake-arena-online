export interface User {
  id: string;
  username: string;
  email: string;
}

export interface LeaderboardEntry {
  id: string;
  username: string;
  score: number;
  mode: "walls" | "pass-through";
  timestamp: number;
}

export interface ActivePlayer {
  id: string;
  username: string;
  score: number;
  mode: "walls" | "pass-through";
  snake: { x: number; y: number }[];
  food: { x: number; y: number };
  isGameOver: boolean;
}

// Mock storage
let currentUser: User | null = null;
const users: Map<string, { password: string; user: User }> = new Map();
const leaderboard: LeaderboardEntry[] = [];

// Initialize with some mock data
const mockLeaderboard: LeaderboardEntry[] = [
  { id: "1", username: "NeonMaster", score: 850, mode: "walls", timestamp: Date.now() - 3600000 },
  { id: "2", username: "CyberSnake", score: 720, mode: "pass-through", timestamp: Date.now() - 7200000 },
  { id: "3", username: "PixelHunter", score: 680, mode: "walls", timestamp: Date.now() - 10800000 },
  { id: "4", username: "GridRunner", score: 590, mode: "pass-through", timestamp: Date.now() - 14400000 },
  { id: "5", username: "RetroGamer", score: 540, mode: "walls", timestamp: Date.now() - 18000000 },
  { id: "6", username: "TronLegend", score: 490, mode: "pass-through", timestamp: Date.now() - 21600000 },
  { id: "7", username: "ArcadeKing", score: 450, mode: "walls", timestamp: Date.now() - 25200000 },
  { id: "8", username: "NeonNinja", score: 420, mode: "pass-through", timestamp: Date.now() - 28800000 },
];

leaderboard.push(...mockLeaderboard);

// Auth API
export const mockAuth = {
  login: async (email: string, password: string): Promise<{ user: User; error?: string }> => {
    await new Promise((resolve) => setTimeout(resolve, 500)); // Simulate network delay

    const userEntry = users.get(email);
    if (!userEntry || userEntry.password !== password) {
      return { user: null as any, error: "Invalid credentials" };
    }

    currentUser = userEntry.user;
    localStorage.setItem("mockUser", JSON.stringify(currentUser));
    return { user: userEntry.user };
  },

  signup: async (username: string, email: string, password: string): Promise<{ user: User; error?: string }> => {
    await new Promise((resolve) => setTimeout(resolve, 500));

    if (users.has(email)) {
      return { user: null as any, error: "User already exists" };
    }

    const newUser: User = {
      id: Math.random().toString(36).substring(7),
      username,
      email,
    };

    users.set(email, { password, user: newUser });
    currentUser = newUser;
    localStorage.setItem("mockUser", JSON.stringify(currentUser));
    return { user: newUser };
  },

  logout: async (): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    currentUser = null;
    localStorage.removeItem("mockUser");
  },

  getCurrentUser: (): User | null => {
    if (currentUser) return currentUser;
    
    const stored = localStorage.getItem("mockUser");
    if (stored) {
      currentUser = JSON.parse(stored);
      return currentUser;
    }
    
    return null;
  },
};

// Leaderboard API
export const mockLeaderboardAPI = {
  getLeaderboard: async (): Promise<LeaderboardEntry[]> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    return [...leaderboard].sort((a, b) => b.score - a.score);
  },

  submitScore: async (score: number, mode: "walls" | "pass-through"): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    
    const user = mockAuth.getCurrentUser();
    if (!user) throw new Error("Not authenticated");

    const entry: LeaderboardEntry = {
      id: Math.random().toString(36).substring(7),
      username: user.username,
      score,
      mode,
      timestamp: Date.now(),
    };

    leaderboard.push(entry);
  },

  getTopScores: async (limit: number = 10): Promise<LeaderboardEntry[]> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    return [...leaderboard]
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  },
};

// Spectate API with mock active players
const generateMockSnake = () => {
  const length = Math.floor(Math.random() * 8) + 3;
  const startX = Math.floor(Math.random() * 15) + 3;
  const startY = Math.floor(Math.random() * 15) + 3;
  
  const snake = [{ x: startX, y: startY }];
  for (let i = 1; i < length; i++) {
    snake.push({ x: startX - i, y: startY });
  }
  
  return snake;
};

const mockPlayers: ActivePlayer[] = [
  {
    id: "p1",
    username: "NeonMaster",
    score: 230,
    mode: "walls",
    snake: generateMockSnake(),
    food: { x: Math.floor(Math.random() * 20), y: Math.floor(Math.random() * 20) },
    isGameOver: false,
  },
  {
    id: "p2",
    username: "CyberSnake",
    score: 180,
    mode: "pass-through",
    snake: generateMockSnake(),
    food: { x: Math.floor(Math.random() * 20), y: Math.floor(Math.random() * 20) },
    isGameOver: false,
  },
  {
    id: "p3",
    username: "PixelHunter",
    score: 150,
    mode: "walls",
    snake: generateMockSnake(),
    food: { x: Math.floor(Math.random() * 20), y: Math.floor(Math.random() * 20) },
    isGameOver: false,
  },
  {
    id: "p4",
    username: "GridRunner",
    score: 120,
    mode: "pass-through",
    snake: generateMockSnake(),
    food: { x: Math.floor(Math.random() * 20), y: Math.floor(Math.random() * 20) },
    isGameOver: false,
  },
];

export const mockSpectateAPI = {
  getActivePlayers: async (): Promise<ActivePlayer[]> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    return mockPlayers.map(player => ({
      ...player,
      snake: generateMockSnake(), // Simulate movement
      score: player.score + Math.floor(Math.random() * 20),
    }));
  },

  watchPlayer: async (playerId: string): Promise<ActivePlayer | null> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    const player = mockPlayers.find(p => p.id === playerId);
    if (!player) return null;
    
    return {
      ...player,
      snake: generateMockSnake(),
      score: player.score + Math.floor(Math.random() * 20),
    };
  },
};
