"""Spectate database model"""
from datetime import datetime
from pydantic import BaseModel
from typing import Literal
from app.schemas.spectate import Position


class ActivePlayerInDB(BaseModel):
    """Active player stored in database"""
    id: str
    username: str
    score: int
    mode: Literal["walls", "pass-through"]
    snake: list[Position]
    food: Position
    is_game_over: bool = False
    direction: Literal["UP", "DOWN", "LEFT", "RIGHT"] = "RIGHT"
    started_at: datetime

    class Config:
        from_attributes = True
