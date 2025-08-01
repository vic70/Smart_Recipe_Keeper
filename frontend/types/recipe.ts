export enum RecipeType {
  APPETIZER = 'appetizer',
  MAIN_COURSE = 'main_course',
  SIDE_DISH = 'side_dish',
  SOUP = 'soup',
  SALAD = 'salad',
  DESSERT = 'dessert',
  BEVERAGE = 'beverage',
  SAUCE = 'sauce',
  BREAD = 'bread',
  SNACK = 'snack',
}

export enum Difficulty {
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard',
}

export interface Ingredient {
  name: string;
  quantity: string;
  unit: string;
  notes?: string;
}

export interface Instruction {
  step_number: number;
  instruction: string;
  time?: number;
}

export interface Nutrition {
  calories?: number;
  protein?: string;
  carbs?: string;
  fat?: string;
}

export interface RecipeSource {
  type: string;
  url?: string;
  platform?: string;
}

export interface Recipe {
  _id: string;
  user_id: string;
  title: string;
  description?: string;
  recipe_type?: RecipeType;
  cuisine?: string;
  dietary_info: string[];
  prep_time?: number;
  cook_time?: number;
  total_time?: number;
  servings?: number;
  difficulty?: Difficulty;
  ingredients: Ingredient[];
  instructions: Instruction[];
  nutrition?: Nutrition;
  images: string[];
  source?: RecipeSource;
  tags: string[];
  notes?: string;
  is_favorite: boolean;
  created_at: string;
  updated_at: string;
}

export interface RecipeCreate {
  url: string;
  notes?: string;
  tags?: string[];
}

export interface RecipeUpdate extends Partial<Omit<Recipe, '_id' | 'user_id' | 'created_at' | 'updated_at'>> {}

// Recipe type labels for UI
export const RECIPE_TYPE_LABELS: Record<RecipeType, string> = {
  [RecipeType.APPETIZER]: 'Appetizer',
  [RecipeType.MAIN_COURSE]: 'Main Course',
  [RecipeType.SIDE_DISH]: 'Side Dish',
  [RecipeType.SOUP]: 'Soup',
  [RecipeType.SALAD]: 'Salad',
  [RecipeType.DESSERT]: 'Dessert',
  [RecipeType.BEVERAGE]: 'Beverage',
  [RecipeType.SAUCE]: 'Sauce & Dressing',
  [RecipeType.BREAD]: 'Bread & Baked Goods',
  [RecipeType.SNACK]: 'Snack',
};

// Recipe type descriptions
export const RECIPE_TYPE_DESCRIPTIONS: Record<RecipeType, string> = {
  [RecipeType.APPETIZER]: 'Small dishes served before the main course',
  [RecipeType.MAIN_COURSE]: 'Primary dish of a meal, usually substantial',
  [RecipeType.SIDE_DISH]: 'Accompaniments to the main course',
  [RecipeType.SOUP]: 'Liquid-based dishes, hot or cold',
  [RecipeType.SALAD]: 'Cold dishes with mixed vegetables, fruits, or proteins',
  [RecipeType.DESSERT]: 'Sweet dishes typically served after a meal',
  [RecipeType.BEVERAGE]: 'Drinks including smoothies, cocktails, teas',
  [RecipeType.SAUCE]: 'Condiments, dressings, and sauces',
  [RecipeType.BREAD]: 'Baked goods including breads, rolls, and pastries',
  [RecipeType.SNACK]: 'Light foods eaten between meals',
};