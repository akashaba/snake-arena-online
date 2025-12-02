"""User schemas"""
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Literal


class User(BaseModel):
    """User model"""
    id: str
    username: str
    email: EmailStr
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """User profile"""
    id: str
    username: str
    created_at: datetime
    total_games: int = 0
    highest_score: int = 0
    favorite_mode: Literal["walls", "pass-through"] | None = None


class UserStats(BaseModel):
    """User statistics"""
    total_games: int = 0
    total_score: int = 0
    average_score: float = 0.0
    highest_score: int = 0
    wall_mode_games: int = 0
    pass_through_mode_games: int = 0
    best_wall_score: int = 0
    best_pass_through_score: int = 0
    rank: int | None = None
