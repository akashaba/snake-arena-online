"""Spectate router"""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import ActivePlayer, ErrorResponse

router = APIRouter(prefix="/spectate", tags=["Spectate"])


@router.get(
    "/players",
    response_model=list[ActivePlayer],
)
async def get_active_players(
    mode: Literal["walls", "pass-through"] | None = Query(None, description="Filter by game mode"),
    db: AsyncSession = Depends(get_db),
):
    """Get all currently active players"""
    players = await crud.active_players.get_active_players(db, mode=mode)
    
    return [
        ActivePlayer(
            id=p.id,
            username=p.username,
            score=p.score,
            mode=p.mode,
            snake=p.snake,
            food=p.food,
            is_game_over=p.is_game_over,
            direction=p.direction,
            started_at=p.started_at
        )
        for p in players
    ]


@router.get(
    "/players/{player_id}",
    response_model=ActivePlayer,
    responses={
        404: {"model": ErrorResponse, "description": "Player not found or not currently playing"},
    }
)
async def watch_player(player_id: str, db: AsyncSession = Depends(get_db)):
    """Get detailed game state for a specific active player"""
    player = await crud.active_players.get_active_player(db, player_id)
    
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found or not currently playing",
        )
    
    return ActivePlayer(
        id=player.id,
        username=player.username,
        score=player.score,
        mode=player.mode,
        snake=player.snake,
        food=player.food,
        is_game_over=player.is_game_over,
        direction=player.direction,
        started_at=player.started_at
    )
