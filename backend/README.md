# Neon Snake Arena - Backend

FastAPI backend for the Neon Snake Arena Online game.

## Features

- **Authentication**: JWT-based authentication with login, signup, and logout
- **Leaderboard**: Score tracking with filtering and pagination
- **Spectate Mode**: Watch active players in real-time
- **User Profiles**: Public profiles and detailed statistics
- **Mock Database**: In-memory storage for development (easily replaceable with real database)

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **python-jose**: JWT token handling
- **bcrypt**: Secure password hashing
- **pytest**: Testing framework with 32 comprehensive tests

## Project Structure

```
backend/
├── app/
│   ├── routers/          # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── leaderboard.py # Leaderboard endpoints
│   │   ├── spectate.py   # Spectate endpoints
│   │   └── users.py      # User profile endpoints
│   ├── schemas/          # Pydantic request/response models
│   ├── models/           # Database models
│   ├── utils/            # Authentication utilities
│   ├── config.py         # Application configuration
│   └── database.py       # Mock database (in-memory)
├── tests/                # Pytest tests
│   ├── test_auth.py
│   ├── test_leaderboard.py
│   ├── test_spectate.py
│   ├── test_users.py
│   └── test_integration.py
├── main.py               # FastAPI application
├── pyproject.toml        # Project dependencies
└── pytest.ini            # Pytest configuration
```

## Getting Started

### Prerequisites

- Python 3.13+
- uv (Python package manager)

### Installation

1. Navigate to the backend directory:
```powershell
cd backend
```

2. Sync dependencies:
```powershell
uv sync
```

### Running the Server

```powershell
uv run python main.py
```

Or with uvicorn directly:
```powershell
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Running Tests

Run all tests:
```powershell
uv run pytest -v
```

Run specific test file:
```powershell
uv run pytest tests/test_auth.py -v
```

Run with coverage:
```powershell
uv run pytest --cov=app --cov-report=html
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/logout` - User logout (requires authentication)
- `GET /api/v1/auth/me` - Get current user (requires authentication)

### Leaderboard

- `GET /api/v1/leaderboard` - Get leaderboard with filtering and pagination
- `GET /api/v1/leaderboard/top` - Get top N scores
- `POST /api/v1/leaderboard/scores` - Submit a score (requires authentication)
- `GET /api/v1/leaderboard/user/{userId}` - Get user's scores

### Spectate

- `GET /api/v1/spectate/players` - Get all active players
- `GET /api/v1/spectate/players/{playerId}` - Watch specific player

### User Profiles

- `GET /api/v1/users/{userId}` - Get user profile
- `GET /api/v1/users/{userId}/stats` - Get user statistics

## Mock Users

The mock database includes 8 test users (all with password `password123`):

- neon@example.com (NeonMaster)
- cyber@example.com (CyberSnake)
- pixel@example.com (PixelHunter)
- grid@example.com (GridRunner)
- retro@example.com (RetroGamer)
- tron@example.com (TronLegend)
- arcade@example.com (ArcadeKing)
- ninja@example.com (NeonNinja)

## Configuration

Configuration can be customized in `app/config.py` or via environment variables:

- `SECRET_KEY`: JWT secret key (change in production!)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 1440 = 24 hours)
- `CORS_ORIGINS`: Allowed CORS origins

## Testing

The project includes 32 comprehensive tests covering:

- ✅ Authentication (login, signup, logout, current user)
- ✅ Leaderboard (get, filter, pagination, submit scores)
- ✅ Spectate (active players, watch specific player)
- ✅ User profiles (profiles, statistics, rankings)
- ✅ Integration tests (complete user flows)

All tests use a fresh database instance to ensure isolation.

## Replacing the Mock Database

The current implementation uses an in-memory mock database. To replace with a real database:

1. Install a database driver (e.g., `uv add sqlalchemy asyncpg` for PostgreSQL)
2. Create database models in `app/models/`
3. Update `app/database.py` with real database connection
4. Implement CRUD operations
5. Update routers to use new database operations

## CORS Configuration

The API is configured to allow requests from:
- http://localhost:5173 (Vite default)
- http://localhost:3000 (React default)
- http://127.0.0.1:5173
- http://127.0.0.1:3000

Modify `app/config.py` to add more origins as needed.

## Development

### Adding New Endpoints

1. Define Pydantic schemas in `app/schemas/`
2. Create router in `app/routers/`
3. Register router in `main.py`
4. Add tests in `tests/`

### Code Style

The project follows standard Python conventions:
- Type hints for all function parameters and returns
- Docstrings for all modules, classes, and functions
- Pydantic for data validation
- FastAPI dependency injection for authentication

## License

MIT

## Contributing

Contributions welcome! Please ensure all tests pass before submitting PRs.
