from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.recipe import Recipe
from app.models.user import User
from app.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeList
)
from app.core.security import get_current_active_user
from app.core.gemini import GeminiService
from app.services.extractors import ExtractorFactory

router = APIRouter()


@router.post("/extract", response_model=RecipeResponse)
async def extract_recipe(
    recipe_data: RecipeCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Extract recipe from URL and save it"""
    # Get appropriate extractor
    extractor = ExtractorFactory.get_extractor(recipe_data.url)
    if not extractor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported URL type"
        )
    
    try:
        # Extract content from URL
        content = await extractor.extract(recipe_data.url)
        
        # Process with Gemini
        gemini_service = GeminiService()
        recipe_info = await gemini_service.extract_recipe_data(content)
        
        if not recipe_info:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Failed to extract recipe information"
            )
        
        # Create recipe document
        recipe = Recipe(
            user_id=str(current_user.id),
            **recipe_info,
            tags=recipe_data.tags if recipe_data.tags else [],
            notes=recipe_data.notes
        )
        
        # Save to database
        await recipe.insert()
        
        return RecipeResponse(
            _id=str(recipe.id),
            user_id=recipe.user_id,
            title=recipe.title,
            description=recipe.description,
            recipe_type=recipe.recipe_type,
            cuisine=recipe.cuisine,
            dietary_info=recipe.dietary_info,
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            total_time=recipe.total_time,
            servings=recipe.servings,
            difficulty=recipe.difficulty,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            nutrition=recipe.nutrition,
            images=recipe.images,
            source=recipe.source,
            tags=recipe.tags,
            notes=recipe.notes,
            is_favorite=recipe.is_favorite,
            created_at=recipe.created_at,
            updated_at=recipe.updated_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process recipe: {str(e)}"
        )


@router.get("/", response_model=RecipeList)
async def get_recipes(
    current_user: User = Depends(get_current_active_user),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    recipe_type: Optional[str] = None,
    cuisine: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    tags: Optional[List[str]] = Query(None)
):
    """Get user's recipes with pagination and filtering"""
    # Build query
    query_dict = {"user_id": str(current_user.id)}
    
    if search:
        query_dict["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}}
        ]
    
    if recipe_type:
        query_dict["recipe_type"] = recipe_type
    
    if cuisine:
        query_dict["cuisine"] = cuisine
    
    if is_favorite is not None:
        query_dict["is_favorite"] = is_favorite
    
    if tags:
        query_dict["tags"] = {"$in": tags}
    
    # Calculate pagination
    skip = (page - 1) * per_page
    
    # Get total count
    total = await Recipe.find(query_dict).count()
    
    # Get recipes
    recipes = await Recipe.find(query_dict).skip(skip).limit(per_page).sort("-created_at").to_list()
    
    # Convert to response format
    recipe_responses = []
    for recipe in recipes:
        recipe_responses.append(RecipeResponse(
            _id=str(recipe.id),
            user_id=recipe.user_id,
            title=recipe.title,
            description=recipe.description,
            recipe_type=recipe.recipe_type,
            cuisine=recipe.cuisine,
            dietary_info=recipe.dietary_info,
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            total_time=recipe.total_time,
            servings=recipe.servings,
            difficulty=recipe.difficulty,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            nutrition=recipe.nutrition,
            images=recipe.images,
            source=recipe.source,
            tags=recipe.tags,
            notes=recipe.notes,
            is_favorite=recipe.is_favorite,
            created_at=recipe.created_at,
            updated_at=recipe.updated_at
        ))
    
    total_pages = (total + per_page - 1) // per_page
    
    return RecipeList(
        recipes=recipe_responses,
        total=total,
        page=page,
        per_page=per_page,
        pages=total_pages
    )


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific recipe"""
    recipe = await Recipe.find_one({
        "_id": recipe_id,
        "user_id": str(current_user.id)
    })
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    return RecipeResponse(
        _id=str(recipe.id),
        user_id=recipe.user_id,
        title=recipe.title,
        description=recipe.description,
        recipe_type=recipe.recipe_type,
        cuisine=recipe.cuisine,
        dietary_info=recipe.dietary_info,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        total_time=recipe.total_time,
        servings=recipe.servings,
        difficulty=recipe.difficulty,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        nutrition=recipe.nutrition,
        images=recipe.images,
        source=recipe.source,
        tags=recipe.tags,
        notes=recipe.notes,
        is_favorite=recipe.is_favorite,
        created_at=recipe.created_at,
        updated_at=recipe.updated_at
    )


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: str,
    recipe_update: RecipeUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a recipe"""
    recipe = await Recipe.find_one({
        "_id": recipe_id,
        "user_id": str(current_user.id)
    })
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Update fields
    update_data = recipe_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recipe, field, value)
    
    recipe.updated_at = datetime.utcnow()
    await recipe.save()
    
    return RecipeResponse(
        _id=str(recipe.id),
        user_id=recipe.user_id,
        title=recipe.title,
        description=recipe.description,
        recipe_type=recipe.recipe_type,
        cuisine=recipe.cuisine,
        dietary_info=recipe.dietary_info,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        total_time=recipe.total_time,
        servings=recipe.servings,
        difficulty=recipe.difficulty,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        nutrition=recipe.nutrition,
        images=recipe.images,
        source=recipe.source,
        tags=recipe.tags,
        notes=recipe.notes,
        is_favorite=recipe.is_favorite,
        created_at=recipe.created_at,
        updated_at=recipe.updated_at
    )


@router.delete("/{recipe_id}")
async def delete_recipe(
    recipe_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a recipe"""
    recipe = await Recipe.find_one({
        "_id": recipe_id,
        "user_id": str(current_user.id)
    })
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    await recipe.delete()
    
    return {"message": "Recipe deleted successfully"}