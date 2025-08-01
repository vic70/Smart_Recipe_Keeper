from typing import List, Optional
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field, BaseModel


class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: str
    notes: Optional[str] = None


class Instruction(BaseModel):
    step_number: int
    instruction: str
    time: Optional[int] = None  # Time in minutes


class Nutrition(BaseModel):
    calories: Optional[int] = None
    protein: Optional[str] = None
    carbs: Optional[str] = None
    fat: Optional[str] = None


class RecipeSource(BaseModel):
    type: str  # website, youtube, instagram, manual
    url: Optional[str] = None
    platform: Optional[str] = None


class Recipe(Document):
    """Recipe document model for MongoDB"""
    
    # Basic Information
    user_id: Indexed(str)
    title: str
    description: Optional[str] = None
    recipe_type: Optional[str] = None  # appetizer, main_course, side_dish, soup, salad, dessert, beverage, sauce, bread, snack
    cuisine: Optional[str] = None
    
    # Dietary Information
    dietary_info: List[str] = Field(default_factory=list)
    
    # Time Information
    prep_time: Optional[int] = None  # in minutes
    cook_time: Optional[int] = None  # in minutes
    total_time: Optional[int] = None  # in minutes
    
    # Recipe Details
    servings: Optional[int] = None
    difficulty: Optional[str] = None  # easy, medium, hard
    
    # Ingredients and Instructions
    ingredients: List[Ingredient] = Field(default_factory=list)
    instructions: List[Instruction] = Field(default_factory=list)
    
    # Nutrition
    nutrition: Optional[Nutrition] = None
    
    # Media
    images: List[str] = Field(default_factory=list)
    
    # Source Information
    source: Optional[RecipeSource] = None
    
    # Organization
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    is_favorite: bool = False
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "recipes"
        indexes = [
            "user_id",
            "title",
            "recipe_type",
            "cuisine",
            "tags",
            "is_favorite",
            "created_at"
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "title": "Spaghetti Carbonara",
                "description": "Classic Italian pasta dish",
                "recipe_type": "main_course",
                "cuisine": "Italian",
                "dietary_info": ["gluten-free-optional"],
                "prep_time": 15,
                "cook_time": 20,
                "servings": 4,
                "difficulty": "medium",
                "ingredients": [
                    {
                        "name": "Spaghetti",
                        "quantity": "400",
                        "unit": "grams"
                    }
                ],
                "instructions": [
                    {
                        "step_number": 1,
                        "instruction": "Boil water for pasta",
                        "time": 5
                    }
                ],
                "tags": ["pasta", "italian", "quick"]
            }
        }