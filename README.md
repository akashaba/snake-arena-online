# 🎮 Neon Snake Arena Online

A multiplayer Snake game with neon cyberpunk aesthetics, featuring real-time leaderboards, spectate mode, and user authentication.

![Snake Game](https://img.shields.io/badge/Game-Snake-00ff00?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)

## ✨ Features

- 🐍 **Classic Snake Gameplay** with modern neon aesthetics
- 🎯 **Two Game Modes**: Walls (classic) and Pass-through
- 🏆 **Real-time Leaderboard** with score tracking
- 👀 **Spectate Mode** to watch other players
- 🔐 **User Authentication** with JWT tokens
- 📊 **Player Statistics** and rankings
- 📱 **Responsive Design** for desktop and mobile

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.13+
- **uv** (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/akashaba/snake-arena-online.git
cd snake-arena-online

# Install root dependencies (concurrently)
npm install

# Install backend dependencies
cd backend
uv sync
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Run the Application

**Start both servers at once:**
```bash
npm run dev
```

This will start:
- 🔧 **Backend**: http://localhost:8000
- 🎮 **Frontend**: http://localhost:8080

**Or run separately:**
```bash
# Terminal 1 - Backend
npm run backend

# Terminal 2 - Frontend
npm run frontend
```

## 🎯 Quick Test

1. Open http://localhost:8080
2. Login with test account:
   - Email: `neon@example.com`
   - Password: `password123`
3. Start playing! 🎮

## 📁 Project Structure

```
snake-arena-online/
├── backend/              # FastAPI backend
│   ├── app/              # Application code
│   │   ├── routers/      # API endpoints
│   │   ├── schemas/      # Pydantic models
│   │   ├── models/       # Database models
│   │   └── utils/        # Utilities (auth, etc.)
│   ├── tests/            # 32 comprehensive tests
│   └── main.py           # Entry point
│
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   ├── hooks/        # Game logic hooks
│   │   └── lib/          # Game engine
│   └── public/
│
├── package.json          # Root scripts
├── QUICKSTART.md         # Quick start guide
└── INTEGRATION.md        # Integration details
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **pytest** - Testing (32 tests, 100% pass)

### Frontend
- **React** + **TypeScript**
- **Vite** - Build tool
- **Tailwind CSS** + **shadcn/ui**
- **React Router** - Routing

## 📜 Available Scripts

From the root directory:

```bash
npm run dev              # Start both servers
npm run backend          # Start backend only
npm run frontend         # Start frontend only
npm run test:backend     # Run backend tests
npm run test:frontend    # Run frontend tests
npm run build:frontend   # Build frontend for production
```

## 🔑 Test Accounts

All test users have password: `password123`

Top players:
- `neon@example.com` - NeonMaster (1250 points)
- `king@example.com` - SnakeKing (1180 points)
- `gridmaster@example.com` - GridMaster (1050 points)

20 total test users available!

## 🌐 API Documentation

When the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: `backend/openapi.yaml`

## 🧪 Testing

**Backend (32 tests):**
```bash
npm run test:backend
```

**Frontend:**
```bash
npm run test:frontend
```

**All tests passing:** ✅

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started quickly
- **[INTEGRATION.md](INTEGRATION.md)** - Integration details
- **[backend/README.md](backend/README.md)** - Backend documentation
- **[frontend/README.md](frontend/README.md)** - Frontend documentation

## 🔧 Configuration

### Backend (`.env` or `app/config.py`)
```python
SECRET_KEY = "your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
```

### Frontend (`frontend/.env`)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🎮 Game Controls

- **Arrow Keys** or **WASD** - Control snake direction
- **Space** - Pause/Resume
- **Click Mode Button** - Switch between Walls/Pass-through

## 🚧 Roadmap

- [ ] Replace mock database with PostgreSQL
- [ ] Add WebSocket support for real-time updates
- [ ] Implement token refresh mechanism
- [ ] Add more game modes and power-ups
- [ ] Add player chat/messaging
- [ ] Deploy to production
- [ ] Add game replays
- [ ] Mobile app versions

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 👨‍💻 Development

**Guidelines:**
- Backend: Follow `AGENTS.md` - use `uv` for dependencies
- Frontend: Standard npm workflow
- Add tests for all new features
- Update documentation

**Development workflow:**
```bash
# Start dev servers with hot reload
npm run dev

# Make changes - both servers auto-reload

# Run tests
npm run test:backend
npm run test:frontend

# Commit changes
git add .
git commit -m "feat: add new feature"
git push
```

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python 3.13+ is installed
- Run `uv sync` in backend directory
- Ensure port 8000 is available

**Frontend won't start:**
- Check Node.js 18+ is installed
- Run `npm install` in frontend directory
- Ensure port 8080 is available

**Can't login:**
- Verify backend is running
- Check browser console for errors
- Clear localStorage and try again

## 📫 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review INTEGRATION.md for detailed setup

---

**Made with ❤️ for the AI Dev Tools Zoomcamp**

**Ready to play? Run `npm run dev` and visit http://localhost:8080 🎮**
