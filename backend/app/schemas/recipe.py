from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.core.constants import RecipeType, Difficulty


class IngredientBase(BaseModel):
    name: str
    quantity: str
    unit: str
    notes: Optional[str] = None


class InstructionBase(BaseModel):
    step_number: int
    instruction: str
    time: Optional[int] = None


class NutritionBase(BaseModel):
    calories: Optional[int] = None
    protein: Optional[str] = None
    carbs: Optional[str] = None
    fat: Optional[str] = None


class RecipeSourceBase(BaseModel):
    type: str
    url: Optional[str] = None
    platform: Optional[str] = None


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    recipe_type: Optional[str] = None
    cuisine: Optional[str] = None
    dietary_info: List[str] = Field(default_factory=list)
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    ingredients: List[IngredientBase] = Field(default_factory=list)
    instructions: List[InstructionBase] = Field(default_factory=list)
    nutrition: Optional[NutritionBase] = None
    images: List[str] = Field(default_factory=list)
    source: Optional[RecipeSourceBase] = None
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    is_favorite: bool = False
    
    @validator('recipe_type')
    def validate_recipe_type(cls, v):
        if v and v not in [rt.value for rt in RecipeType]:
            # Try to map common variations
            type_mapping = {
                'entree': RecipeType.MAIN_COURSE.value,
                'main': RecipeType.MAIN_COURSE.value,
                'starter': RecipeType.APPETIZER.value,
                'drink': RecipeType.BEVERAGE.value,
                'dressing': RecipeType.SAUCE.value,
                'condiment': RecipeType.SAUCE.value,
            }
            v = type_mapping.get(v.lower(), v)
        return v
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v and v not in [d.value for d in Difficulty]:
            return None
        return v


class RecipeCreate(BaseModel):
    """Schema for creating a recipe from URL"""
    url: str
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe"""
    title: Optional[str] = None
    description: Optional[str] = None
    recipe_type: Optional[str] = None
    cuisine: Optional[str] = None
    dietary_info: Optional[List[str]] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    ingredients: Optional[List[IngredientBase]] = None
    instructions: Optional[List[InstructionBase]] = None
    nutrition: Optional[NutritionBase] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    is_favorite: Optional[bool] = None


class RecipeResponse(RecipeBase):
    """Schema for recipe response"""
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True


class RecipeList(BaseModel):
    """Schema for paginated recipe list"""
    recipes: List[RecipeResponse]
    total: int
    page: int
    per_page: int
    pages: int