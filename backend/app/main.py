from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.models.user import User
from app.models.recipe import Recipe
from app.api import auth, recipes, users
from app.core.security import get_limiter

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database connection on startup"""
    # Startup
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client.get_default_database()
    
    await init_beanie(
        database=database,
        document_models=[User, Recipe]
    )
    
    yield
    
    # Shutdown
    client.close()


# Create FastAPI app
app = FastAPI(
    title="Smart Recipe Keeper API",
    description="API for managing and extracting recipes from various sources",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
limiter = get_limiter()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers
app.include_router(auth.router, prefix=f"{settings.api_prefix}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.api_prefix}/users", tags=["Users"])
app.include_router(recipes.router, prefix=f"{settings.api_prefix}/recipes", tags=["Recipes"])


@app.get("/")
async def root():
    return {
        "message": "Smart Recipe Keeper API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}