"""CRUD operations for users"""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import User


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    """Get user by ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get user by email"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Get user by username"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    user_id: str,
    username: str,
    email: str,
    hashed_password: str,
) -> User:
    """Create a new user"""
    db_user = User(
        id=user_id,
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_count(db: AsyncSession) -> int:
    """Get total number of users"""
    result = await db.execute(select(func.count(User.id)))
    return result.scalar_one()
