"""User profile router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import ErrorResponse, UserProfile, UserStats

router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "/{user_id}",
    response_model=UserProfile,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
    }
)
async def get_user_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get public profile information for a user"""
    user = await crud.users.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Get user scores to calculate profile stats
    scores = await crud.leaderboard.get_user_scores(db, user_id)
    
    total_games = len(scores)
    highest_score = max((s.score for s in scores), default=0)
    
    # Calculate favorite mode
    wall_games = sum(1 for s in scores if s.mode == "walls")
    pass_through_games = total_games - wall_games
    favorite_mode = "walls" if wall_games >= pass_through_games and wall_games > 0 else (
        "pass-through" if pass_through_games > 0 else None
    )
    
    return UserProfile(
        id=user.id,
        username=user.username,
        created_at=user.created_at,
        total_games=total_games,
        highest_score=highest_score,
        favorite_mode=favorite_mode
    )


@router.get(
    "/{user_id}/stats",
    response_model=UserStats,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
    }
)
async def get_user_stats(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get detailed statistics for a user"""
    user = await crud.users.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Get user scores
    scores = await crud.leaderboard.get_user_scores(db, user_id)
    
    total_games = len(scores)
    total_score = sum(s.score for s in scores)
    average_score = total_score / total_games if total_games > 0 else 0.0
    highest_score = max((s.score for s in scores), default=0)
    
    # Mode-specific stats
    wall_scores = [s for s in scores if s.mode == "walls"]
    pass_through_scores = [s for s in scores if s.mode == "pass-through"]
    
    wall_mode_games = len(wall_scores)
    pass_through_mode_games = len(pass_through_scores)
    best_wall_score = max((s.score for s in wall_scores), default=0)
    best_pass_through_score = max((s.score for s in pass_through_scores), default=0)
    
    # Calculate rank
    all_entries, _ = await crud.leaderboard.get_leaderboard(db, limit=10000, offset=0)
    unique_users = {}
    for entry in all_entries:
        if entry.user_id not in unique_users or entry.score > unique_users[entry.user_id]:
            unique_users[entry.user_id] = entry.score
    
    sorted_users = sorted(unique_users.items(), key=lambda x: -x[1])
    rank = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == user_id), None)
    
    return UserStats(
        total_games=total_games,
        total_score=total_score,
        average_score=round(average_score, 2),
        highest_score=highest_score,
        wall_mode_games=wall_mode_games,
        pass_through_mode_games=pass_through_mode_games,
        best_wall_score=best_wall_score,
        best_pass_through_score=best_pass_through_score,
        rank=rank
    )
