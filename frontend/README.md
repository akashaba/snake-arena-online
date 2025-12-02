# Neon Snake Arena - Frontend

React frontend for the Neon Snake Arena Online game.

## Project info

**URL**: https://lovable.dev/projects/ca33877e-d432-440e-86b8-f5f0fa3fba75

## Features

- **Multiplayer Snake Game**: Classic snake game with neon cyberpunk aesthetics
- **Two Game Modes**: Play with walls (classic) or pass-through mode
- **Real-time Leaderboard**: Track your scores and compete with other players
- **Spectate Mode**: Watch active players in real-time
- **Authentication**: JWT-based user authentication
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Vite**: Fast build tool and dev server
- **TypeScript**: Type-safe JavaScript
- **React**: UI framework
- **shadcn-ui**: Beautiful UI components
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **React Query**: API state management (installed but not yet utilized)

## Backend Integration

The frontend connects to a FastAPI backend running on `http://localhost:8000`. The API integration includes:

- **Authentication**: Login, signup, logout, and token management
- **Leaderboard**: Fetch and submit scores with filtering and pagination
- **Spectate**: Watch active players in real-time
- **User Profiles**: View user statistics and rankings

### API Configuration

The API base URL is configured in `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Change this for production deployments.

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend server running on `http://localhost:8000` (see backend README)

### Installation

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Running the Development Server

```powershell
npm run dev
```

The app will be available at `http://localhost:8080`

### Building for Production

```powershell
npm run build
```

Built files will be in the `dist/` directory.

### Running Tests

```powershell
npm test
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── game/         # Game-specific components
│   │   └── ui/           # shadcn-ui components
│   ├── config/           # Configuration files
│   │   └── api.ts        # API endpoints and base URL
│   ├── hooks/            # Custom React hooks
│   │   └── useGameLogic.ts  # Core game logic
│   ├── lib/              # Utility libraries
│   │   └── gameEngine.ts # Game engine logic
│   ├── pages/            # Page components
│   │   ├── Auth.tsx      # Login/Signup page
│   │   ├── Index.tsx     # Main game page
│   │   ├── Leaderboard.tsx
│   │   └── Spectate.tsx
│   ├── services/         # API services
│   │   ├── api.ts        # Backend API client
│   │   └── mockBackend.ts # (Legacy) Mock backend
│   └── main.tsx          # Entry point
├── .env                  # Environment variables
└── package.json
```

## API Service

The `services/api.ts` file provides:

- **Token Management**: Automatic JWT token injection in requests
- **Error Handling**: Unified error handling with 401 auto-logout
- **Type Safety**: Full TypeScript types matching backend API
- **Auto-conversion**: Converts ISO timestamps to JavaScript timestamps

### Usage Example

```typescript
import { authAPI, leaderboardAPI, spectateAPI } from '@/services/api';

// Login
const { user, token, error } = await authAPI.login(email, password);

// Get leaderboard
const entries = await leaderboardAPI.getLeaderboard({ limit: 20 });

// Submit score
await leaderboardAPI.submitScore(score, mode);

// Get active players
const players = await spectateAPI.getActivePlayers();
```

## Test Users

You can login with any of these test accounts (password: `password123`):

- neon@example.com (NeonMaster)
- king@example.com (SnakeKing)
- wizard@example.com (SnakeWizard)
- viper@example.com (CyberViper)
- And 16 more users...

## Development Notes

### Authentication Flow

1. User logs in via `/auth` page
2. JWT token is stored in `localStorage` as `authToken`
3. User data stored in `localStorage` as `currentUser`
4. All API requests automatically include `Authorization: Bearer <token>` header
5. On 401 response, token is cleared and user redirected to login

### Game Score Submission

- Scores are automatically submitted when game ends (if user is authenticated)
- Failed submissions show error toast but don't interrupt gameplay
- Submissions include score and game mode (walls/pass-through)

### Spectate Mode

- Polls backend every 2 seconds for active player updates
- Displays mini game boards with real-time snake positions
- Automatically cleans up polling on component unmount

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/ca33877e-d432-440e-86b8-f5f0fa3fba75) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/ca33877e-d432-440e-86b8-f5f0fa3fba75) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)
