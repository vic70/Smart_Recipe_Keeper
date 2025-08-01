from typing import Optional, List
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field, EmailStr


class User(Document):
    """User document model for MongoDB"""
    
    # Authentication
    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    hashed_password: str
    
    # Profile Information
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    
    # Account Status
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False
    
    # Preferences
    preferred_cuisines: List[str] = Field(default_factory=list)
    dietary_restrictions: List[str] = Field(default_factory=list)
    
    # OAuth Information (for future use)
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "username",
            "created_at"
        ]
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "preferred_cuisines": ["Italian", "Mexican"],
                "dietary_restrictions": ["vegetarian"]
            }
        }