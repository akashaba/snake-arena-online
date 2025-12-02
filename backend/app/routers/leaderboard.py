"""Leaderboard router"""
import uuid
from datetime import datetime
from typing import Literal
from fastapi import APIRouter, Query, HTTPException, status
from app.schemas import (
    LeaderboardEntry,
    LeaderboardResponse,
    SubmitScoreRequest,
    ErrorResponse,
)
from app.models import LeaderboardEntryInDB
from app.database import db
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
):
    """Get full leaderboard with filtering and pagination"""
    entries, total = db.get_leaderboard(mode=mode, limit=limit, offset=offset)
    
    return LeaderboardResponse(
        entries=[
            LeaderboardEntry(
                id=e.id,
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
):
    """Get top N scores from the leaderboard"""
    entries, _ = db.get_leaderboard(mode=mode, limit=limit, offset=0)
    
    return [
        LeaderboardEntry(
            id=e.id,
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
):
    """Submit a new score to the leaderboard"""
    entry_id = str(uuid.uuid4())
    
    new_entry = LeaderboardEntryInDB(
        id=entry_id,
        user_id=current_user.id,
        username=current_user.username,
        score=request.score,
        mode=request.mode,
        timestamp=datetime.utcnow()
    )
    
    db.add_score(new_entry)
    
    return LeaderboardEntry(
        id=new_entry.id,
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
):
    """Get all scores for a specific user"""
    # Check if user exists
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    entries = db.get_user_scores(user_id, mode=mode)
    
    return [
        LeaderboardEntry(
            id=e.id,
            user_id=e.user_id,
            username=e.username,
            score=e.score,
            mode=e.mode,
            timestamp=e.timestamp
        )
        for e in entries
    ]
