"""Integration tests for user endpoints"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def create_test_user(client: AsyncClient, username: str, email: str) -> tuple[str, str]:
    """Helper to create a test user and return token and user_id"""
    signup_data = {
        "username": username,
        "email": email,
        "password": "testpassword123",
    }
    response = await client.post("/api/v1/auth/signup", json=signup_data)
    data = response.json()
    return data["token"], data["user"]["id"]


@pytest.mark.asyncio
async def test_get_user_profile(client: AsyncClient, db_session: AsyncSession):
    """Test retrieving user profile"""
    token, user_id = await create_test_user(client, "testuser", "test@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Submit some scores
    for score in [100, 200, 150]:
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": "walls"},
            headers=headers,
        )

    # Get profile
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser"
    assert data["total_games"] == 3
    assert data["highest_score"] == 200
    assert data["favorite_mode"] == "walls"


@pytest.mark.asyncio
async def test_get_user_stats(client: AsyncClient, db_session: AsyncSession):
    """Test retrieving detailed user statistics"""
    token, user_id = await create_test_user(client, "testuser", "test@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Submit scores in different modes
    wall_scores = [100, 200, 150]
    passthrough_scores = [80, 120]

    for score in wall_scores:
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": "walls"},
            headers=headers,
        )

    for score in passthrough_scores:
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": "pass-through"},
            headers=headers,
        )

    # Get stats
    response = await client.get(f"/api/v1/users/{user_id}/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_games"] == 5
    assert data["total_score"] == 650
    assert data["average_score"] == 130.0
    assert data["highest_score"] == 200
    assert data["wall_mode_games"] == 3
    assert data["pass_through_mode_games"] == 2
    assert data["best_wall_score"] == 200
    assert data["best_pass_through_score"] == 120
    assert data["rank"] == 1  # Only user


@pytest.mark.asyncio
async def test_get_user_rank(client: AsyncClient, db_session: AsyncSession):
    """Test user ranking calculation"""
    # Create 3 users with different high scores
    users = [
        ("player1", "player1@example.com", 300),
        ("player2", "player2@example.com", 200),
        ("player3", "player3@example.com", 100),
    ]

    user_ids = []
    for username, email, score in users:
        token, user_id = await create_test_user(client, username, email)
        user_ids.append(user_id)
        headers = {"Authorization": f"Bearer {token}"}
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": "walls"},
            headers=headers,
        )

    # Check ranks
    response = await client.get(f"/api/v1/users/{user_ids[0]}/stats")
    assert response.json()["rank"] == 1  # player1 with 300

    response = await client.get(f"/api/v1/users/{user_ids[1]}/stats")
    assert response.json()["rank"] == 2  # player2 with 200

    response = await client.get(f"/api/v1/users/{user_ids[2]}/stats")
    assert response.json()["rank"] == 3  # player3 with 100


@pytest.mark.asyncio
async def test_get_nonexistent_user(client: AsyncClient, db_session: AsyncSession):
    """Test getting profile for non-existent user"""
    response = await client.get("/api/v1/users/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_profile_no_games(client: AsyncClient, db_session: AsyncSession):
    """Test user profile when user has no games played"""
    token, user_id = await create_test_user(client, "newuser", "new@example.com")

    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_games"] == 0
    assert data["highest_score"] == 0
    assert data["favorite_mode"] is None


@pytest.mark.asyncio
async def test_favorite_mode_calculation(client: AsyncClient, db_session: AsyncSession):
    """Test favorite mode calculation based on game count"""
    token, user_id = await create_test_user(client, "player", "player@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Play more walls games
    for _ in range(3):
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": 100, "mode": "walls"},
            headers=headers,
        )

    for _ in range(1):
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": 100, "mode": "pass-through"},
            headers=headers,
        )

    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["favorite_mode"] == "walls"

    # Play more pass-through games to change favorite
    for _ in range(3):
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": 100, "mode": "pass-through"},
            headers=headers,
        )

    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["favorite_mode"] == "pass-through"
