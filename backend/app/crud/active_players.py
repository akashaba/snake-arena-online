"""CRUD operations for active players"""
from datetime import datetime, timedelta, timezone
from typing import Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import ActivePlayer


async def get_active_players(
    db: AsyncSession,
    mode: Literal["walls", "pass-through"] | None = None,
) -> list[ActivePlayer]:
    """Get all active players"""
    query = select(ActivePlayer).where(ActivePlayer.is_game_over == False)
    
    if mode:
        query = query.where(ActivePlayer.mode == mode)
    
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_active_player(
    db: AsyncSession,
    player_id: str,
) -> ActivePlayer | None:
    """Get a specific active player"""
    result = await db.execute(
        select(ActivePlayer).where(
            ActivePlayer.id == player_id,
            ActivePlayer.is_game_over == False,
        )
    )
    return result.scalar_one_or_none()


async def create_active_player(
    db: AsyncSession,
    player_id: str,
    username: str,
    mode: Literal["walls", "pass-through"],
    snake: dict,
    food: dict,
    direction: Literal["UP", "DOWN", "LEFT", "RIGHT"] = "RIGHT",
) -> ActivePlayer:
    """Create a new active player"""
    player = ActivePlayer(
        id=player_id,
        username=username,
        score=0,
        mode=mode,
        snake=snake,
        food=food,
        is_game_over=False,
        direction=direction,
        started_at=datetime.now(timezone.utc),
    )
    db.add(player)
    await db.commit()
    await db.refresh(player)
    return player


async def update_player_state(
    db: AsyncSession,
    player_id: str,
    score: int | None = None,
    snake: dict | None = None,
    food: dict | None = None,
    direction: Literal["UP", "DOWN", "LEFT", "RIGHT"] | None = None,
) -> ActivePlayer | None:
    """Update player game state"""
    result = await db.execute(
        select(ActivePlayer).where(ActivePlayer.id == player_id)
    )
    player = result.scalar_one_or_none()
    
    if not player:
        return None
    
    if score is not None:
        player.score = score
    if snake is not None:
        player.snake = snake
    if food is not None:
        player.food = food
    if direction is not None:
        player.direction = direction
    
    await db.commit()
    await db.refresh(player)
    return player


async def mark_game_over(
    db: AsyncSession,
    player_id: str,
) -> ActivePlayer | None:
    """Mark player's game as over"""
    result = await db.execute(
        select(ActivePlayer).where(ActivePlayer.id == player_id)
    )
    player = result.scalar_one_or_none()
    
    if not player:
        return None
    
    player.is_game_over = True
    await db.commit()
    await db.refresh(player)
    return player


async def cleanup_inactive_players(
    db: AsyncSession,
    inactive_minutes: int = 30,
) -> int:
    """Remove inactive players (game over or started too long ago)"""
    cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=inactive_minutes)
    
    query = select(ActivePlayer).where(
        (ActivePlayer.is_game_over == True) | (ActivePlayer.started_at < cutoff_time)
    )
    result = await db.execute(query)
    players = list(result.scalars().all())
    
    for player in players:
        await db.delete(player)
    
    await db.commit()
    return len(players)
