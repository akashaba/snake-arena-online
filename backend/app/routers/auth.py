"""Authentication router"""
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from app.schemas import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
    User,
    ErrorResponse,
)
from app.models import UserInDB
from app.database import db
from app.utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    CurrentUser,
)
from fastapi import Depends
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    }
)
async def login(request: LoginRequest):
    """Authenticate a user with email and password"""
    # Get user by email
    user_in_db = db.get_user_by_email(request.email)
    
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
async def signup(request: SignupRequest):
    """Create a new user account"""
    # Check if user already exists
    existing_user = db.get_user_by_email(request.email)
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(request.password)
    
    new_user = UserInDB(
        id=user_id,
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    
    db.create_user(new_user)
    
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
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Invalidate the current user session"""
    token = credentials.credentials
    
    # Add token to blacklist
    db.blacklist_token(token)
    
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
