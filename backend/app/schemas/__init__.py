"""Pydantic schemas for request/response validation"""
from .auth import LoginRequest, SignupRequest, TokenResponse
from .user import User, UserProfile, UserStats
from .leaderboard import LeaderboardEntry, LeaderboardResponse, SubmitScoreRequest
from .spectate import Position, ActivePlayer
from .common import ErrorResponse, ValidationErrorResponse

__all__ = [
    "LoginRequest",
    "SignupRequest",
    "TokenResponse",
    "User",
    "UserProfile",
    "UserStats",
    "LeaderboardEntry",
    "LeaderboardResponse",
    "SubmitScoreRequest",
    "Position",
    "ActivePlayer",
    "ErrorResponse",
    "ValidationErrorResponse",
]
