"""Authentication router"""
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.config import settings
from app.database import get_db
from app.schemas import (
    ErrorResponse,
    LoginRequest,
    SignupRequest,
    TokenResponse,
    User,
)
from app.utils import (
    CurrentUser,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    }
)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate a user with email and password"""
    # Get user by email
    user_in_db = await crud.users.get_user_by_email(db, request.email)
    
    if not user_in_db or not verify_password(request.password, user_in_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user_in_db.id})
    
    user = User(
        id=user_in_db.id,
        username=user_in_db.username,
        email=user_in_db.email,
        created_at=user_in_db.created_at
    )
    
    return TokenResponse(user=user, token=access_token)


@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "User already exists"},
    }
)
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    """Create a new user account"""
    # Check if user already exists
    existing_user = await crud.users.get_user_by_email(db, request.email)
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(request.password)
    
    new_user = await crud.users.create_user(
        db,
        user_id=user_id,
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
    )
    
    # Create access token
    access_token = create_access_token(data={"sub": user_id})
    
    user = User(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        created_at=new_user.created_at
    )
    
    return TokenResponse(user=user, token=access_token)


@router.post(
    "/logout",
    response_model=dict,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    }
)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """Invalidate the current user session"""
    token = credentials.credentials
    
    # Decode token to get expiration
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    exp_timestamp = payload.get("exp")
    if exp_timestamp:
        expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    else:
        # Default to token expiration time from settings
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    # Add token to blacklist
    await crud.token_blacklist.blacklist_token(db, token, expires_at)
    
    return {"message": "Logged out successfully"}


@router.get(
    "/me",
    response_model=User,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    }
)
async def get_me(current_user: CurrentUser):
    """Get currently authenticated user's information"""
    return current_user
