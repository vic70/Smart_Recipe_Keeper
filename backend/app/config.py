from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    # MongoDB
    mongodb_url: str = "mongodb://localhost:27017/smart_recipe_keeper"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Google Gemini API
    gemini_api_key: Optional[str] = None
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    # External APIs (for future use)
    youtube_api_key: Optional[str] = None
    instagram_client_id: Optional[str] = None
    instagram_client_secret: Optional[str] = None
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()