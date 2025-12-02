# Neon Snake Arena - Quick Start

## 🎮 What is this?

A multiplayer Snake game with neon cyberpunk aesthetics, featuring:
- Classic Snake gameplay with two modes (walls & pass-through)
- Real-time leaderboard and score tracking
- Spectate mode to watch other players
- User authentication and profiles

## 🚀 Quick Start

### Option 1: Start Both Servers (Recommended)

```bash
npm run dev
```

This uses `concurrently` to run both backend and frontend with color-coded output.

### Option 2: Start Manually

**Terminal 1 - Backend:**
```bash
npm run backend
# or: cd backend && uv run python run.py
```

**Terminal 2 - Frontend:**
```bash
npm run frontend
# or: cd frontend && npm run dev
```

## 🌐 Access the App

- **Frontend:** http://localhost:8080
- **Backend API Docs:** http://localhost:8000/docs
- **Backend Health:** http://localhost:8000/health

## 🔑 Test Login

Use any of these accounts (password: `password123`):

```
neon@example.com     - NeonMaster (Top Player - 1250)
king@example.com     - SnakeKing (2nd Place - 1180)
wizard@example.com   - SnakeWizard
viper@example.com    - CyberViper
gridmaster@example.com - GridMaster
```

Or create your own account via signup!

## 📋 Features to Test

1. **Signup/Login** - Create account or login with test credentials
2. **Play Game** - Start game in walls or pass-through mode
3. **Submit Score** - Finish game to auto-submit score to leaderboard
4. **View Leaderboard** - See top 20 players with scores
5. **Spectate** - Watch 10 active players in real-time
6. **Logout** - Clear session and return to login

## 🛠️ Tech Stack

**Frontend:**
- React + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui
- React Router

**Backend:**
- FastAPI (Python)
- JWT Authentication
- Bcrypt password hashing
- In-memory mock database

## 📁 Project Structure

```
snake-arena-online/
├── backend/           # FastAPI backend
│   ├── app/           # Application code
│   ├── tests/         # 32 comprehensive tests
│   └── main.py        # Entry point
├── frontend/          # React frontend
│   ├── src/           # Source code
│   │   ├── components/ # UI components
│   │   ├── pages/     # Page components
│   │   ├── services/  # API client
│   │   └── hooks/     # Game logic
│   └── .env           # API configuration
└── INTEGRATION.md     # Detailed integration guide
```

## 🧪 Testing

**Backend Tests (32 tests):**
```bash
npm run test:backend
# or: cd backend && uv run pytest -v
```

**Frontend Tests:**
```bash
npm run test:frontend
# or: cd frontend && npm test
```

## 📦 Available Scripts

From the root directory:

```bash
npm run dev              # Start both servers with concurrently
npm run backend          # Start only backend
npm run frontend         # Start only frontend
npm run test:backend     # Run backend tests
npm run test:frontend    # Run frontend tests
npm run build:frontend   # Build frontend for production
```

## 📚 Documentation

- **Frontend README:** `frontend/README.md`
- **Backend README:** `backend/README.md`
- **Integration Guide:** `INTEGRATION.md`
- **API Documentation:** http://localhost:8000/docs (when running)
- **OpenAPI Spec:** `backend/openapi.yaml`

## 🐛 Troubleshooting

**Backend won't start:**
- Ensure Python 3.13+ installed
- Run `uv sync` in backend directory
- Check port 8000 is available

**Frontend won't start:**
- Ensure Node.js 18+ installed
- Run `npm install` in frontend directory
- Check port 8080 is available

**Can't connect to backend:**
- Verify backend is running: http://localhost:8000/health
- Check `.env` file: `VITE_API_BASE_URL=http://localhost:8000/api/v1`
- Clear browser cache and localStorage

**Token expired errors:**
- Logout and login again
- Tokens expire after 24 hours
- Clear localStorage: `localStorage.clear()`

## 🎯 Development Guide

**Follow AGENTS.md for backend development:**
```powershell
# Install dependencies
uv sync

# Add new package
uv add <package-name>

# Run Python files
uv run python <file>
```

**Frontend development:**
```powershell
# Install dependencies
npm install

# Run dev server (auto-reload)
npm run dev

# Build for production
npm run build
```

## 🔮 Future Enhancements

- [ ] Replace mock database with PostgreSQL/MongoDB
- [ ] Add WebSocket support for real-time updates
- [ ] Implement token refresh mechanism
- [ ] Add React Query for better API state management
- [ ] Add offline support with service workers
- [ ] Deploy to production (Azure/AWS/Vercel)
- [ ] Add more game modes and power-ups
- [ ] Add chat/messaging between players
- [ ] Add game replays

## 📝 Notes

- **Mock Data:** Backend uses in-memory storage (resets on restart)
- **CORS:** Configured for localhost development
- **Security:** Change secret keys for production!
- **Performance:** Spectate mode polls every 2 seconds

## 🤝 Contributing

1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Test both frontend and backend
5. Ensure all tests pass before committing

## 📄 License

MIT

---

**Ready to play? Start the servers and visit http://localhost:8080 🎮**
