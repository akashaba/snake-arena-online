"""Leaderboard database model"""
from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class LeaderboardEntryInDB(BaseModel):
    """Leaderboard entry stored in database"""
    id: str
    user_id: str
    username: str
    score: int
    mode: Literal["walls", "pass-through"]
    timestamp: datetime

    class Config:
        from_attributes = True
