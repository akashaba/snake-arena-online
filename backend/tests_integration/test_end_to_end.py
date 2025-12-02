"""End-to-end integration tests"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud


@pytest.mark.asyncio
async def test_complete_game_flow(client: AsyncClient, db_session: AsyncSession):
    """Test a complete game flow from signup to score submission"""
    # 1. User signs up
    signup_data = {
        "username": "GamePlayer",
        "email": "gamer@example.com",
        "password": "securepassword",
    }
    response = await client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 201
    token = response.json()["token"]
    user_id = response.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Verify user can access protected endpoints
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200

    # 3. User starts a game (create active player)
    await crud.active_players.create_active_player(
        db_session,
        player_id=f"game-{user_id}",
        username="GamePlayer",
        mode="walls",
        snake=[{"x": 10, "y": 10}],
        food={"x": 15, "y": 15},
        direction="RIGHT",
    )

    # 4. User can be found in spectate mode
    response = await client.get("/api/v1/spectate/players")
    assert response.status_code == 200
    players = response.json()
    assert len(players) == 1
    assert players[0]["username"] == "GamePlayer"

    # 5. User finishes game and submits score
    response = await client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 250, "mode": "walls"},
        headers=headers,
    )
    assert response.status_code == 201

    # 6. Score appears in leaderboard
    response = await client.get("/api/v1/leaderboard")
    assert response.status_code == 200
    leaderboard = response.json()
    assert leaderboard["total"] == 1
    assert leaderboard["entries"][0]["score"] == 250

    # 7. User profile is updated
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    profile = response.json()
    assert profile["total_games"] == 1
    assert profile["highest_score"] == 250


@pytest.mark.asyncio
async def test_multiple_users_competition(client: AsyncClient, db_session: AsyncSession):
    """Test multiple users competing on leaderboard"""
    users_data = [
        ("Player1", "player1@example.com", [100, 150, 200]),
        ("Player2", "player2@example.com", [180, 220, 190]),
        ("Player3", "player3@example.com", [50, 80, 120]),
    ]

    user_ids = []
    for username, email, scores in users_data:
        # Signup
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "username": username,
                "email": email,
                "password": "password123",
            },
        )
        token = response.json()["token"]
        user_id = response.json()["user"]["id"]
        user_ids.append(user_id)
        headers = {"Authorization": f"Bearer {token}"}

        # Submit scores
        for score in scores:
            await client.post(
                "/api/v1/leaderboard/scores",
                json={"score": score, "mode": "walls"},
                headers=headers,
            )

    # Check leaderboard
    response = await client.get("/api/v1/leaderboard")
    assert response.status_code == 200
    leaderboard = response.json()
    assert leaderboard["total"] == 9  # 3 users × 3 scores

    # Top score should be 220 (Player2)
    assert leaderboard["entries"][0]["score"] == 220
    assert leaderboard["entries"][0]["username"] == "Player2"

    # Check rankings
    response = await client.get(f"/api/v1/users/{user_ids[1]}/stats")
    assert response.json()["rank"] == 1  # Player2 with highest score 220

    response = await client.get(f"/api/v1/users/{user_ids[0]}/stats")
    assert response.json()["rank"] == 2  # Player1 with highest score 200

    response = await client.get(f"/api/v1/users/{user_ids[2]}/stats")
    assert response.json()["rank"] == 3  # Player3 with highest score 120


@pytest.mark.asyncio
async def test_user_session_management(client: AsyncClient, db_session: AsyncSession):
    """Test user session lifecycle"""
    # Signup
    response = await client.post(
        "/api/v1/auth/signup",
        json={
            "username": "SessionUser",
            "email": "session@example.com",
            "password": "password123",
        },
    )
    token1 = response.json()["token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Verify token works
    response = await client.get("/api/v1/auth/me", headers=headers1)
    assert response.status_code == 200

    # Login to get same user (signup and login use same JWT mechanism)
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "session@example.com",
            "password": "password123",
        },
    )
    token2 = response.json()["token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Both tokens should work initially
    response = await client.get("/api/v1/auth/me", headers=headers1)
    assert response.status_code == 200
    response = await client.get("/api/v1/auth/me", headers=headers2)
    assert response.status_code == 200

    # Logout first token
    response = await client.post("/api/v1/auth/logout", headers=headers1)
    assert response.status_code == 200

    # First token should be invalid after logout
    response = await client.get("/api/v1/auth/me", headers=headers1)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_data_consistency(client: AsyncClient, db_session: AsyncSession):
    """Test data consistency across endpoints"""
    # Create user
    response = await client.post(
        "/api/v1/auth/signup",
        json={
            "username": "ConsistentUser",
            "email": "consistent@example.com",
            "password": "password123",
        },
    )
    token = response.json()["token"]
    user_id = response.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    # Submit scores
    scores = [100, 200, 150, 180, 220]
    for score in scores:
        await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": "walls"},
            headers=headers,
        )

    # Check consistency across endpoints

    # 1. User profile shows correct counts
    response = await client.get(f"/api/v1/users/{user_id}")
    profile = response.json()
    assert profile["total_games"] == 5
    assert profile["highest_score"] == 220

    # 2. User stats show correct data
    response = await client.get(f"/api/v1/users/{user_id}/stats")
    stats = response.json()
    assert stats["total_games"] == 5
    assert stats["total_score"] == sum(scores)
    assert stats["average_score"] == sum(scores) / len(scores)
    assert stats["highest_score"] == 220

    # 3. User scores endpoint shows all scores
    response = await client.get(f"/api/v1/leaderboard/user/{user_id}")
    user_scores = response.json()
    assert len(user_scores) == 5
    assert user_scores[0]["score"] == 220  # Sorted descending

    # 4. All scores appear in leaderboard
    response = await client.get("/api/v1/leaderboard?limit=10")
    leaderboard = response.json()
    user_entries = [e for e in leaderboard["entries"] if e["user_id"] == user_id]
    assert len(user_entries) == 5


@pytest.mark.asyncio
async def test_multiple_score_submissions(client: AsyncClient, db_session: AsyncSession):
    """Test handling multiple score submissions sequentially"""
    # Create user
    response = await client.post(
        "/api/v1/auth/signup",
        json={
            "username": "MultiScoreUser",
            "email": "multiscore@example.com",
            "password": "password123",
        },
    )
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Submit multiple scores sequentially
    scores = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for score in scores:
        response = await client.post(
            "/api/v1/leaderboard/scores",
            json={"score": score, "mode": "walls"},
            headers=headers,
        )
        assert response.status_code == 201

    # Verify all scores were recorded
    response = await client.get("/api/v1/leaderboard?limit=20")
    assert response.json()["total"] == 10
