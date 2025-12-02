"""Authentication schemas"""
from pydantic import BaseModel, EmailStr, Field
from .user import User


class LoginRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class SignupRequest(BaseModel):
    """Signup request"""
    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    """Token response"""
    user: User
    token: str


class LogoutResponse(BaseModel):
    """Logout response"""
    message: str = "Logged out successfully"
