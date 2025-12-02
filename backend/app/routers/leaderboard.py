"""Leaderboard router"""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import (
    ErrorResponse,
    LeaderboardEntry,
    LeaderboardResponse,
    SubmitScoreRequest,
)
from app.utils import CurrentUser

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get(
    "",
    response_model=LeaderboardResponse,
)
async def get_leaderboard(
    mode: Literal["walls", "pass-through"] | None = Query(None, description="Filter by game mode"),
    limit: int = Query(20, ge=1, le=100, description="Maximum entries to return"),
    offset: int = Query(0, ge=0, description="Number of entries to skip"),
    db: AsyncSession = Depends(get_db),
):
    """Get full leaderboard with filtering and pagination"""
    entries, total = await crud.leaderboard.get_leaderboard(
        db, mode=mode, limit=limit, offset=offset
    )
    
    return LeaderboardResponse(
        entries=[
            LeaderboardEntry(
                id=str(e.id),
                user_id=e.user_id,
                username=e.username,
                score=e.score,
                mode=e.mode,
                timestamp=e.timestamp
            )
            for e in entries
        ],
        total=total,
        limit=limit,
        offset=offset
    )


@router.get(
    "/top",
    response_model=list[LeaderboardEntry],
)
async def get_top_scores(
    limit: int = Query(10, ge=1, le=100, description="Number of top scores"),
    mode: Literal["walls", "pass-through"] | None = Query(None, description="Filter by game mode"),
    db: AsyncSession = Depends(get_db),
):
    """Get top N scores from the leaderboard"""
    entries, _ = await crud.leaderboard.get_leaderboard(
        db, mode=mode, limit=limit, offset=0
    )
    
    return [
        LeaderboardEntry(
            id=str(e.id),
            user_id=e.user_id,
            username=e.username,
            score=e.score,
            mode=e.mode,
            timestamp=e.timestamp
        )
        for e in entries
    ]


@router.post(
    "/scores",
    response_model=LeaderboardEntry,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    }
)
async def submit_score(
    request: SubmitScoreRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Submit a new score to the leaderboard"""
    new_entry = await crud.leaderboard.add_score(
        db,
        user_id=current_user.id,
        username=current_user.username,
        score=request.score,
        mode=request.mode,
    )
    
    return LeaderboardEntry(
        id=str(new_entry.id),
        user_id=new_entry.user_id,
        username=new_entry.username,
        score=new_entry.score,
        mode=new_entry.mode,
        timestamp=new_entry.timestamp
    )


@router.get(
    "/user/{user_id}",
    response_model=list[LeaderboardEntry],
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
    }
)
async def get_user_scores(
    user_id: str,
    mode: Literal["walls", "pass-through"] | None = Query(None, description="Filter by game mode"),
    db: AsyncSession = Depends(get_db),
):
    """Get all scores for a specific user"""
    # Check if user exists
    user = await crud.users.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    entries = await crud.leaderboard.get_user_scores(db, user_id, mode=mode)
    
    return [
        LeaderboardEntry(
            id=str(e.id),
            user_id=e.user_id,
            username=e.username,
            score=e.score,
            mode=e.mode,
            timestamp=e.timestamp
        )
        for e in entries
    ]
