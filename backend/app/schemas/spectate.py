"""Spectate schemas"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal


class Position(BaseModel):
    """Grid position"""
    x: int = Field(..., ge=0, le=19)
    y: int = Field(..., ge=0, le=19)


class ActivePlayer(BaseModel):
    """Active player game state"""
    id: str
    username: str
    score: int = Field(..., ge=0)
    mode: Literal["walls", "pass-through"]
    snake: list[Position]
    food: Position
    is_game_over: bool = False
    direction: Literal["UP", "DOWN", "LEFT", "RIGHT"] | None = None
    started_at: datetime | None = None

    class Config:
        from_attributes = True
