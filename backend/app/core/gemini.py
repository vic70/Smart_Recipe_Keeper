import google.generativeai as genai
from typing import Dict, Any, Optional
import json
from app.config import get_settings
from app.schemas.recipe import RecipeBase


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        settings = get_settings()
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    async def extract_recipe_data(self, content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract structured recipe data from raw content using Gemini"""
        
        if not self.model:
            raise ValueError("Gemini API key not configured")
        
        # Prepare the prompt
        prompt = self._create_extraction_prompt(content)
        
        try:
            response = self.model.generate_content(prompt)
            
            # Parse the response
            recipe_data = self._parse_gemini_response(response.text)
            
            # Merge with any existing structured data
            if content.get('recipe_data'):
                recipe_data = self._merge_recipe_data(recipe_data, content['recipe_data'])
            
            # Add source information
            recipe_data['source'] = {
                'type': content.get('content_type', 'website'),
                'url': content.get('url', ''),
                'platform': content.get('platform_data', {}).get('platform', 'web')
            }
            
            return recipe_data
            
        except Exception as e:
            print(f"Gemini extraction error: {str(e)}")
            return None
    
    def _create_extraction_prompt(self, content: Dict[str, Any]) -> str:
        """Create a prompt for Gemini to extract recipe data"""
        
        prompt = f"""
        Extract recipe information from the following content and return it as a valid JSON object.
        
        Content Title: {content.get('title', '')}
        Content Description: {content.get('description', '')}
        
        Raw Content:
        {content.get('raw_content', '')[:5000]}  # Limit content length
        
        Please extract and structure the following information in JSON format:
        {{
            "title": "Recipe title",
            "description": "Brief description of the recipe",
            "recipe_type": "One of: appetizer, main_course, side_dish, soup, salad, dessert, beverage, sauce, bread, snack",
            "cuisine": "Type of cuisine (e.g., Italian, Mexican, Asian)",
            "dietary_info": ["Array of dietary tags like vegetarian, vegan, gluten-free"],
            "prep_time": "Preparation time in minutes (number only)",
            "cook_time": "Cooking time in minutes (number only)",
            "total_time": "Total time in minutes (number only)",
            "servings": "Number of servings (number only)",
            "difficulty": "One of: easy, medium, hard",
            "ingredients": [
                {{
                    "name": "Ingredient name",
                    "quantity": "Amount (e.g., 2, 1/2)",
                    "unit": "Unit of measurement (e.g., cups, tbsp, grams)",
                    "notes": "Optional notes (e.g., 'diced', 'room temperature')"
                }}
            ],
            "instructions": [
                {{
                    "step_number": 1,
                    "instruction": "Step description",
                    "time": "Optional time in minutes for this step"
                }}
            ],
            "nutrition": {{
                "calories": "Number of calories per serving",
                "protein": "Protein in grams",
                "carbs": "Carbohydrates in grams",
                "fat": "Fat in grams"
            }},
            "tags": ["Array of relevant tags"],
            "notes": "Any additional notes or tips"
        }}
        
        Important:
        - Extract only factual information present in the content
        - Use null for missing information
        - Ensure all numeric values are numbers, not strings
        - Return only valid JSON without any additional text or formatting
        """
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's response to extract JSON data"""
        try:
            # Try to find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                # If no JSON found, try to parse the entire response
                return json.loads(response_text)
        except json.JSONDecodeError:
            # Return a basic structure if parsing fails
            return {
                "title": "Recipe",
                "description": "Failed to parse recipe data",
                "ingredients": [],
                "instructions": []
            }
    
    def _merge_recipe_data(self, gemini_data: Dict[str, Any], schema_data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge Gemini extracted data with schema.org data"""
        # Schema.org data takes precedence for structured fields
        merged = gemini_data.copy()
        
        # Override with schema data where available
        if schema_data.get('name'):
            merged['title'] = schema_data['name']
        
        if schema_data.get('description'):
            merged['description'] = schema_data['description']
        
        # More merging logic can be added here
        
        return merged