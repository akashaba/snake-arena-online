"""Integration tests for spectate endpoints"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud


@pytest.mark.asyncio
async def test_get_active_players_empty(client: AsyncClient, db_session: AsyncSession):
    """Test getting active players when none exist"""
    response = await client.get("/api/v1/spectate/players")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.asyncio
async def test_get_active_players(client: AsyncClient, db_session: AsyncSession):
    """Test getting list of active players"""
    # Create some active players directly in database
    players = [
        {
            "player_id": "player1",
            "username": "TestPlayer1",
            "mode": "walls",
            "snake": [{"x": 5, "y": 5}, {"x": 4, "y": 5}],
            "food": {"x": 10, "y": 10},
            "direction": "RIGHT",
        },
        {
            "player_id": "player2",
            "username": "TestPlayer2",
            "mode": "pass-through",
            "snake": [{"x": 3, "y": 3}, {"x": 2, "y": 3}],
            "food": {"x": 8, "y": 8},
            "direction": "UP",
        },
    ]

    for player_data in players:
        await crud.active_players.create_active_player(
            db_session,
            player_id=player_data["player_id"],
            username=player_data["username"],
            mode=player_data["mode"],
            snake=player_data["snake"],
            food=player_data["food"],
            direction=player_data["direction"],
        )

    # Get all active players
    response = await client.get("/api/v1/spectate/players")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] in ["TestPlayer1", "TestPlayer2"]
    assert data[0]["is_game_over"] is False


@pytest.mark.asyncio
async def test_get_active_players_filter_by_mode(client: AsyncClient, db_session: AsyncSession):
    """Test filtering active players by game mode"""
    # Create players with different modes
    await crud.active_players.create_active_player(
        db_session,
        player_id="player1",
        username="WallsPlayer",
        mode="walls",
        snake=[{"x": 5, "y": 5}],
        food={"x": 10, "y": 10},
        direction="RIGHT",
    )

    await crud.active_players.create_active_player(
        db_session,
        player_id="player2",
        username="PassThroughPlayer",
        mode="pass-through",
        snake=[{"x": 3, "y": 3}],
        food={"x": 8, "y": 8},
        direction="UP",
    )

    # Filter by walls mode
    response = await client.get("/api/v1/spectate/players?mode=walls")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "WallsPlayer"
    assert data[0]["mode"] == "walls"

    # Filter by pass-through mode
    response = await client.get("/api/v1/spectate/players?mode=pass-through")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "PassThroughPlayer"
    assert data[0]["mode"] == "pass-through"


@pytest.mark.asyncio
async def test_watch_specific_player(client: AsyncClient, db_session: AsyncSession):
    """Test watching a specific player's game"""
    # Create an active player
    player_id = "test-player-123"
    await crud.active_players.create_active_player(
        db_session,
        player_id=player_id,
        username="WatchedPlayer",
        mode="walls",
        snake=[{"x": 5, "y": 5}, {"x": 4, "y": 5}, {"x": 3, "y": 5}],
        food={"x": 10, "y": 10},
        direction="RIGHT",
    )

    # Update player score
    await crud.active_players.update_player_state(
        db_session,
        player_id=player_id,
        score=150,
    )

    # Watch the player
    response = await client.get(f"/api/v1/spectate/players/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == player_id
    assert data["username"] == "WatchedPlayer"
    assert data["score"] == 150
    assert data["mode"] == "walls"
    assert len(data["snake"]) == 3
    assert data["food"] == {"x": 10, "y": 10}
    assert data["direction"] == "RIGHT"
    assert data["is_game_over"] is False


@pytest.mark.asyncio
async def test_watch_nonexistent_player(client: AsyncClient, db_session: AsyncSession):
    """Test watching a player that doesn't exist"""
    response = await client.get("/api/v1/spectate/players/nonexistent-player")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_game_over_players_not_shown(client: AsyncClient, db_session: AsyncSession):
    """Test that players with game_over=True are not shown"""
    # Create active player
    await crud.active_players.create_active_player(
        db_session,
        player_id="player1",
        username="ActivePlayer",
        mode="walls",
        snake=[{"x": 5, "y": 5}],
        food={"x": 10, "y": 10},
        direction="RIGHT",
    )

    # Create game over player
    player2_id = "player2"
    await crud.active_players.create_active_player(
        db_session,
        player_id=player2_id,
        username="GameOverPlayer",
        mode="walls",
        snake=[{"x": 3, "y": 3}],
        food={"x": 8, "y": 8},
        direction="UP",
    )
    await crud.active_players.mark_game_over(db_session, player2_id)

    # Get active players - should only return active one
    response = await client.get("/api/v1/spectate/players")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "ActivePlayer"

    # Try to watch game over player - should return 404
    response = await client.get(f"/api/v1/spectate/players/{player2_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_player_state_updates(client: AsyncClient, db_session: AsyncSession):
    """Test that player state can be updated"""
    player_id = "test-player"
    await crud.active_players.create_active_player(
        db_session,
        player_id=player_id,
        username="TestPlayer",
        mode="walls",
        snake=[{"x": 5, "y": 5}],
        food={"x": 10, "y": 10},
        direction="RIGHT",
    )

    # Update state
    new_snake = [{"x": 6, "y": 5}, {"x": 5, "y": 5}]
    new_food = {"x": 15, "y": 15}
    await crud.active_players.update_player_state(
        db_session,
        player_id=player_id,
        score=50,
        snake=new_snake,
        food=new_food,
        direction="UP",
    )

    # Verify updates
    response = await client.get(f"/api/v1/spectate/players/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 50
    assert data["snake"] == new_snake
    assert data["food"] == new_food
    assert data["direction"] == "UP"
