"""CRUD operations for leaderboard"""
from datetime import datetime, timezone
from typing import Literal

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import LeaderboardEntry


async def get_leaderboard(
    db: AsyncSession,
    mode: Literal["walls", "pass-through"] | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[LeaderboardEntry], int]:
    """Get leaderboard with filtering and pagination"""
    # Build base query
    query = select(LeaderboardEntry)
    
    if mode:
        query = query.where(LeaderboardEntry.mode == mode)
    
    # Get total count
    count_query = select(func.count(LeaderboardEntry.id))
    if mode:
        count_query = count_query.where(LeaderboardEntry.mode == mode)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    # Apply ordering and pagination
    query = query.order_by(desc(LeaderboardEntry.score), LeaderboardEntry.timestamp)
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    entries = list(result.scalars().all())
    
    return entries, total


async def get_user_scores(
    db: AsyncSession,
    user_id: str,
    mode: Literal["walls", "pass-through"] | None = None,
) -> list[LeaderboardEntry]:
    """Get all scores for a user"""
    query = select(LeaderboardEntry).where(LeaderboardEntry.user_id == user_id)
    
    if mode:
        query = query.where(LeaderboardEntry.mode == mode)
    
    query = query.order_by(desc(LeaderboardEntry.score), LeaderboardEntry.timestamp)
    
    result = await db.execute(query)
    return list(result.scalars().all())


async def add_score(
    db: AsyncSession,
    user_id: str,
    username: str,
    score: int,
    mode: Literal["walls", "pass-through"],
) -> LeaderboardEntry:
    """Add a new score to leaderboard"""
    entry = LeaderboardEntry(
        user_id=user_id,
        username=username,
        score=score,
        mode=mode,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


async def get_top_score_by_user(
    db: AsyncSession,
    user_id: str,
    mode: Literal["walls", "pass-through"] | None = None,
) -> LeaderboardEntry | None:
    """Get user's top score"""
    query = select(LeaderboardEntry).where(LeaderboardEntry.user_id == user_id)
    
    if mode:
        query = query.where(LeaderboardEntry.mode == mode)
    
    query = query.order_by(desc(LeaderboardEntry.score)).limit(1)
    
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def delete_old_scores(
    db: AsyncSession,
    before_date: datetime,
) -> int:
    """Delete scores older than a certain date"""
    query = select(LeaderboardEntry).where(LeaderboardEntry.timestamp < before_date)
    result = await db.execute(query)
    entries = list(result.scalars().all())
    
    for entry in entries:
        await db.delete(entry)
    
    await db.commit()
    return len(entries)
