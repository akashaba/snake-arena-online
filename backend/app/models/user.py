"""User database model"""
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserInDB(BaseModel):
    """User stored in database"""
    id: str
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime

    class Config:
        from_attributes = True
