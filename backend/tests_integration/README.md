# Integration Tests

Comprehensive integration tests for the Snake Arena Online backend API using SQLite in-memory database.

## Overview

These tests validate end-to-end functionality of the application by testing:
- Database operations (SQLAlchemy with SQLite)
- API endpoints (FastAPI routes)
- Authentication flows (JWT + token blacklist)
- Business logic (scoring, ranking, statistics)

## Test Structure

```
tests_integration/
├── conftest.py                      # Test fixtures and configuration
├── test_auth_integration.py         # Authentication flows (6 tests)
├── test_leaderboard_integration.py  # Leaderboard CRUD (7 tests)
├── test_users_integration.py        # User profiles & stats (6 tests)
├── test_spectate_integration.py     # Active player spectate (7 tests)
├── test_end_to_end.py              # Complete workflows (5 tests)
└── README.md                       # This file
```

## Running Tests

### Run all integration tests:
```bash
uv run pytest tests_integration/ -v
```

### Run specific test file:
```bash
uv run pytest tests_integration/test_auth_integration.py -v
```

### Run specific test:
```bash
uv run pytest tests_integration/test_auth_integration.py::test_signup_and_login -v
```

### Run with coverage:
```bash
uv run pytest tests_integration/ --cov=app --cov-report=html
```

## Test Coverage

### Authentication (`test_auth_integration.py`)
- ✅ `test_signup_and_login` - Complete signup → login flow
- ✅ `test_signup_duplicate_email` - Duplicate email returns 409
- ✅ `test_login_invalid_credentials` - Invalid credentials return 401
- ✅ `test_get_current_user` - Get authenticated user profile
- ✅ `test_logout` - Logout blacklists token
- ✅ `test_unauthorized_access` - Missing/invalid token returns 401

### Leaderboard (`test_leaderboard_integration.py`)
- ✅ `test_submit_score` - Submit score and verify in database
- ✅ `test_get_leaderboard` - Get all leaderboard entries
- ✅ `test_get_leaderboard_filtered_by_mode` - Filter by game mode
- ✅ `test_get_leaderboard_pagination` - Pagination with limit/offset
- ✅ `test_get_top_scores` - Get top N scores
- ✅ `test_get_user_scores` - Get all scores for specific user
- ✅ `test_submit_score_requires_auth` - Auth required for submission

### User Profiles (`test_users_integration.py`)
- ✅ `test_get_user_profile` - Get user profile with games
- ✅ `test_get_user_stats` - Calculate total/average scores
- ✅ `test_get_user_rank` - Rank calculation based on highest score
- ✅ `test_get_nonexistent_user` - 404 for nonexistent user
- ✅ `test_user_profile_no_games` - Profile with zero games
- ✅ `test_favorite_mode_calculation` - Favorite mode based on play count

### Spectate (`test_spectate_integration.py`)
- ✅ `test_get_active_players_empty` - Empty list when no active players
- ✅ `test_get_active_players` - Get all active players
- ✅ `test_get_active_players_filter_by_mode` - Filter by game mode
- ✅ `test_watch_specific_player` - Watch specific player's game
- ✅ `test_watch_nonexistent_player` - 404 for nonexistent player
- ✅ `test_game_over_players_not_shown` - Game over players filtered out
- ✅ `test_player_state_updates` - Player state updates correctly

### End-to-End Workflows (`test_end_to_end.py`)
- ✅ `test_complete_game_flow` - Signup → play → spectate → submit score → leaderboard
- ✅ `test_multiple_users_competition` - Multiple users with rankings
- ✅ `test_user_session_management` - Token lifecycle and logout
- ✅ `test_data_consistency` - Data consistency across all endpoints
- ✅ `test_multiple_score_submissions` - Sequential score submissions

## Test Database

Tests use an **in-memory SQLite database** (`sqlite+aiosqlite:///:memory:`) for:
- **Speed**: No disk I/O overhead
- **Isolation**: Each test gets a fresh database
- **Consistency**: No state pollution between tests

### Fixtures

#### `db_session` (function scope)
- Creates all tables before each test
- Yields async session for database operations
- Drops all tables after test cleanup
- Usage: `async def test_example(db_session: AsyncSession):`

#### `client` (function scope)
- AsyncClient for testing FastAPI endpoints
- Overrides `get_db` dependency with test database
- Handles lifespan events (startup/shutdown)
- Usage: `async def test_example(client: AsyncClient):`

#### `event_loop` (session scope)
- Shared event loop for all async tests
- Required for pytest-asyncio

## Helper Functions

### `create_test_user(client: AsyncClient)`
Utility function used across tests to create authenticated test users:
```python
user_data, token, headers = await create_test_user(client, "testuser", "test@example.com")
```

Returns:
- `user_data`: Full user response (id, username, email, etc.)
- `token`: JWT authentication token
- `headers`: Authorization headers for API calls

## Key Testing Patterns

### 1. Authentication Flow
```python
# Signup
response = await client.post("/api/v1/auth/signup", json={...})
token = response.json()["token"]

# Use authenticated endpoints
headers = {"Authorization": f"Bearer {token}"}
response = await client.get("/api/v1/auth/me", headers=headers)
```

### 2. Database Operations
```python
# Create via CRUD
user = await crud.users.create_user(db_session, username, email, password)

# Verify via API
response = await client.get(f"/api/v1/users/{user.id}")
assert response.status_code == 200
```

### 3. Pagination Testing
```python
# Test limit/offset
response = await client.get("/api/v1/leaderboard?limit=5&offset=0")
assert len(response.json()["entries"]) == 5
```

### 4. Business Logic Validation
```python
# Submit scores and verify ranking
await submit_multiple_scores(...)
stats = await client.get(f"/api/v1/users/{user_id}/stats")
assert stats.json()["rank"] == 1  # Highest scorer
```

## CI/CD Integration

These tests are designed for CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Integration Tests
  run: |
    cd backend
    uv run pytest tests_integration/ -v --junitxml=junit.xml
```

## Performance

- **Total tests**: 31
- **Execution time**: ~11 seconds
- **Database setup**: <100ms per test (in-memory)
- **No external dependencies**: All tests self-contained

## Notes

- Tests use `pytest.mark.asyncio` decorator for async support
- Each test gets isolated database (function scope)
- Token blacklist is tested to ensure logout works correctly
- All tests pass with SQLite; PostgreSQL compatibility maintained
- Pydantic v2 warnings present but don't affect functionality

## Future Enhancements

- [ ] Add WebSocket testing for real-time game updates
- [ ] Add load testing with concurrent users
- [ ] Add API versioning tests
- [ ] Add rate limiting tests
- [ ] Add database migration tests with Alembic
- [ ] Add test coverage reporting to CI/CD
