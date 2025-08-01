from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str  # Can be email or username
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferred_cuisines: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None


class UserResponse(UserBase):
    id: str = Field(alias="_id")
    is_active: bool
    is_verified: bool
    preferred_cuisines: List[str]
    dietary_restrictions: List[str]
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        populate_by_name = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None