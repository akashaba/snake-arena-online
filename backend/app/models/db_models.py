"""SQLAlchemy database models."""
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSON as PGJSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class User(Base):
    """User database model."""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationship to leaderboard entries
    leaderboard_entries: Mapped[List["LeaderboardEntry"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_username", "username"),
        Index("idx_email", "email"),
    )


class LeaderboardEntry(Base):
    """Leaderboard entry database model."""
    __tablename__ = "leaderboard_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False)  # Denormalized
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[str] = mapped_column(String(20), nullable=False, default="classic")
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationship to user
    user: Mapped["User"] = relationship(back_populates="leaderboard_entries")

    __table_args__ = (
        Index("idx_score_desc", "score", postgresql_ops={"score": "DESC"}),
        Index("idx_mode_score", "mode", "score", postgresql_ops={"score": "DESC"}),
        Index("idx_timestamp", "timestamp"),
        CheckConstraint("mode IN ('walls', 'pass-through')", name="check_mode"),
    )


class ActivePlayer(Base):
    """Active player database model."""
    __tablename__ = "active_players"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mode: Mapped[str] = mapped_column(String(20), nullable=False, default="classic")
    snake: Mapped[Optional[dict]] = mapped_column(PGJSON, nullable=True)
    food: Mapped[Optional[dict]] = mapped_column(PGJSON, nullable=True)
    is_game_over: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False, default="RIGHT")
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        Index("idx_game_over", "is_game_over"),
        CheckConstraint("mode IN ('walls', 'pass-through')", name="check_active_mode"),
        CheckConstraint("direction IN ('UP', 'DOWN', 'LEFT', 'RIGHT')", name="check_direction"),
    )


class TokenBlacklist(Base):
    """Token blacklist database model."""
    __tablename__ = "token_blacklist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    blacklisted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("idx_token", "token"),
        Index("idx_expires", "expires_at"),
    )
