"""API Routers"""
from .auth import router as auth_router
from .leaderboard import router as leaderboard_router
from .spectate import router as spectate_router
from .users import router as users_router

__all__ = [
    "auth_router",
    "leaderboard_router",
    "spectate_router",
    "users_router",
]
