"""Integration tests for leaderboard endpoints"""
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
async def test_submit_score(client: AsyncClient, db_session: AsyncSession):
    """Test submitting a score to the leaderboard"""
    token, user_id = await create_test_user(client, "player1", "player1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Submit score
    score_data = {
        "score": 100,
        "mode": "walls",
    }
    response = await client.post(
        "/api/v1/leaderboard/scores",
        json=score_data,
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["score"] == 100
    assert data["mode"] == "walls"
    assert data["user_id"] == user_id
    assert data["username"] == "player1"


@pytest.mark.asyncio
async def test_get_leaderboard(client: AsyncClient, db_session: AsyncSession):
    """Test retrieving the leaderboard"""
    # Create multiple users and submit scores
    users = [
        ("player1", "player1@example.com", 100, "walls"),
        ("player2", "player2@example.com", 200, "walls"),
        ("player3", "player3@example.com", 150, "pass-through"),
    ]

    for username, email, score, mode in users:
        token, _ = await create_test_user(client, username, email)
        headers = {"Authorization": f"Bearer {token}"}
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": mode},
            headers=headers,
        )

    # Get full leaderboard
    response = await client.get("/api/v1/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert "entries" in data
    assert "total" in data
    assert data["total"] == 3
    # Should be sorted by score descending
    assert data["entries"][0]["score"] == 200
    assert data["entries"][1]["score"] == 150
    assert data["entries"][2]["score"] == 100


@pytest.mark.asyncio
async def test_get_leaderboard_filtered_by_mode(client: AsyncClient, db_session: AsyncSession):
    """Test filtering leaderboard by game mode"""
    # Create users with different modes
    users = [
        ("player1", "player1@example.com", 100, "walls"),
        ("player2", "player2@example.com", 200, "walls"),
        ("player3", "player3@example.com", 150, "pass-through"),
    ]

    for username, email, score, mode in users:
        token, _ = await create_test_user(client, username, email)
        headers = {"Authorization": f"Bearer {token}"}
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": mode},
            headers=headers,
        )

    # Get walls mode only
    response = await client.get("/api/v1/leaderboard?mode=walls")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    for entry in data["entries"]:
        assert entry["mode"] == "walls"

    # Get pass-through mode only
    response = await client.get("/api/v1/leaderboard?mode=pass-through")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["entries"][0]["mode"] == "pass-through"


@pytest.mark.asyncio
async def test_get_leaderboard_pagination(client: AsyncClient, db_session: AsyncSession):
    """Test leaderboard pagination"""
    # Create 5 users with scores
    for i in range(5):
        token, _ = await create_test_user(client, f"player{i}", f"player{i}@example.com")
        headers = {"Authorization": f"Bearer {token}"}
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": (i + 1) * 10, "mode": "walls"},
            headers=headers,
        )

    # Get first 2 entries
    response = await client.get("/api/v1/leaderboard?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["entries"]) == 2
    assert data["total"] == 5
    assert data["entries"][0]["score"] == 50  # Highest score first

    # Get next 2 entries
    response = await client.get("/api/v1/leaderboard?limit=2&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["entries"]) == 2
    assert data["total"] == 5


@pytest.mark.asyncio
async def test_get_top_scores(client: AsyncClient, db_session: AsyncSession):
    """Test getting top N scores"""
    # Create users with scores
    for i in range(5):
        token, _ = await create_test_user(client, f"player{i}", f"player{i}@example.com")
        headers = {"Authorization": f"Bearer {token}"}
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": (i + 1) * 10, "mode": "walls"},
            headers=headers,
        )

    # Get top 3
    response = await client.get("/api/v1/leaderboard/top?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["score"] == 50
    assert data[1]["score"] == 40
    assert data[2]["score"] == 30


@pytest.mark.asyncio
async def test_get_user_scores(client: AsyncClient, db_session: AsyncSession):
    """Test getting scores for a specific user"""
    token, user_id = await create_test_user(client, "player1", "player1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Submit multiple scores
    scores = [100, 200, 150]
    for score in scores:
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": "walls"},
            headers=headers,
        )

    # Get user scores
    response = await client.get(f"/api/v1/leaderboard/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # Should be sorted by score descending
    assert data[0]["score"] == 200
    assert data[1]["score"] == 150
    assert data[2]["score"] == 100


@pytest.mark.asyncio
async def test_submit_score_requires_auth(client: AsyncClient, db_session: AsyncSession):
    """Test that submitting a score requires authentication"""
    score_data = {
        "score": 100,
        "mode": "walls",
    }
    response = await client.post("/api/v1/leaderboard/scores", json=score_data)
    assert response.status_code == 401  # 401 for missing auth
