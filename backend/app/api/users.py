from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return UserResponse(
        _id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        preferred_cuisines=current_user.preferred_cuisines,
        dietary_restrictions=current_user.dietary_restrictions,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user information"""
    # Update fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    current_user.updated_at = datetime.utcnow()
    await current_user.save()
    
    return UserResponse(
        _id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        preferred_cuisines=current_user.preferred_cuisines,
        dietary_restrictions=current_user.dietary_restrictions,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


@router.delete("/me")
async def delete_current_user(
    current_user: User = Depends(get_current_active_user)
):
    """Delete current user account"""
    # Delete all user's recipes first
    from app.models.recipe import Recipe
    await Recipe.find({"user_id": str(current_user.id)}).delete()
    
    # Delete user
    await current_user.delete()
    
    return {"message": "User account deleted successfully"}