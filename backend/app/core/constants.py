"""Constants used throughout the application"""

from enum import Enum


class RecipeType(str, Enum):
    """Types of recipes based on food nature"""
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    SIDE_DISH = "side_dish"
    SOUP = "soup"
    SALAD = "salad"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SAUCE = "sauce"
    BREAD = "bread"
    SNACK = "snack"


class Difficulty(str, Enum):
    """Recipe difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class DietaryInfo(str, Enum):
    """Common dietary restrictions and preferences"""
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    NUT_FREE = "nut_free"
    LOW_CARB = "low_carb"
    KETO = "keto"
    PALEO = "paleo"
    HALAL = "halal"
    KOSHER = "kosher"
    PESCATARIAN = "pescatarian"


# Recipe type descriptions for better categorization
RECIPE_TYPE_DESCRIPTIONS = {
    RecipeType.APPETIZER: "Small dishes served before the main course",
    RecipeType.MAIN_COURSE: "Primary dish of a meal, usually substantial",
    RecipeType.SIDE_DISH: "Accompaniments to the main course",
    RecipeType.SOUP: "Liquid-based dishes, hot or cold",
    RecipeType.SALAD: "Cold dishes with mixed vegetables, fruits, or proteins",
    RecipeType.DESSERT: "Sweet dishes typically served after a meal",
    RecipeType.BEVERAGE: "Drinks including smoothies, cocktails, teas",
    RecipeType.SAUCE: "Condiments, dressings, and sauces",
    RecipeType.BREAD: "Baked goods including breads, rolls, and pastries",
    RecipeType.SNACK: "Light foods eaten between meals"
}