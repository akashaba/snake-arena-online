"""Leaderboard schemas"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal


class LeaderboardEntry(BaseModel):
    """Leaderboard entry"""
    id: str
    user_id: str
    username: str
    score: int = Field(..., ge=0)
    mode: Literal["walls", "pass-through"]
    timestamp: datetime

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Leaderboard response with pagination"""
    entries: list[LeaderboardEntry]
    total: int
    limit: int
    offset: int


class SubmitScoreRequest(BaseModel):
    """Submit score request"""
    score: int = Field(..., ge=0)
    mode: Literal["walls", "pass-through"]
