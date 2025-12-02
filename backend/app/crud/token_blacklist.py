"""CRUD operations for token blacklist"""
from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import TokenBlacklist


async def blacklist_token(
    db: AsyncSession,
    token: str,
    expires_at: datetime,
) -> TokenBlacklist:
    """Add token to blacklist"""
    blacklisted = TokenBlacklist(
        token=token,
        blacklisted_at=datetime.now(timezone.utc),
        expires_at=expires_at,
    )
    db.add(blacklisted)
    await db.commit()
    await db.refresh(blacklisted)
    return blacklisted


async def is_token_blacklisted(
    db: AsyncSession,
    token: str,
) -> bool:
    """Check if token is blacklisted"""
    result = await db.execute(
        select(TokenBlacklist).where(TokenBlacklist.token == token)
    )
    return result.scalar_one_or_none() is not None


async def cleanup_expired_tokens(
    db: AsyncSession,
) -> int:
    """Remove expired tokens from blacklist"""
    now = datetime.now(timezone.utc)
    
    # Use delete statement directly for efficiency
    stmt = delete(TokenBlacklist).where(TokenBlacklist.expires_at < now)
    result = await db.execute(stmt)
    await db.commit()
    
    return result.rowcount or 0
