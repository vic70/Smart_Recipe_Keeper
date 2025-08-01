# Smart Recipe Keeper - Full Stack Application Plan

## Project Overview
A full-stack application that allows users to save recipes from various sources (URLs, YouTube, Instagram Reels) by extracting content using Gemini API and storing structured data in MongoDB.

## Tech Stack
- **Frontend**: Next.js 14+ with TypeScript, shadcn/ui, Tailwind CSS
- **Backend**: Python FastAPI
- **Database**: MongoDB
- **AI Integration**: Google Gemini API
- **Authentication**: JWT with refresh tokens
- **Deployment**: Vercel (frontend), Railway/Render (backend), MongoDB Atlas

## Core Features

### 1. User Management
- User registration/login with email
- JWT-based authentication
- Profile management
- Password reset functionality
- Social login (Google OAuth) - optional enhancement

### 2. Recipe Import
- Accept multiple input types:
  - Direct recipe URLs (from recipe websites)
  - YouTube video URLs
  - Instagram Reels URLs
  - Manual text input
- Extract content using appropriate methods:
  - Web scraping for recipe sites
  - YouTube Data API for video metadata
  - Instagram API/scraping for reels
- Process content through Gemini API for standardization

### 3. Recipe Data Structure
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "title": "string",
  "description": "string",
  "recipe_type": "appetizer|main_course|side_dish|soup|salad|dessert|beverage|sauce|bread|snack",
  "cuisine": "string",
  "dietary_info": ["vegetarian", "vegan", "gluten-free", etc.],
  "prep_time": "number (minutes)",
  "cook_time": "number (minutes)",
  "servings": "number",
  "difficulty": "easy|medium|hard",
  "ingredients": [
    {
      "name": "string",
      "quantity": "string",
      "unit": "string",
      "notes": "string (optional)"
    }
  ],
  "instructions": [
    {
      "step_number": "number",
      "instruction": "string",
      "time": "number (optional, minutes)"
    }
  ],
  "nutrition": {
    "calories": "number",
    "protein": "string",
    "carbs": "string",
    "fat": "string"
  },
  "source": {
    "type": "url|youtube|instagram|manual",
    "url": "string",
    "platform": "string"
  },
  "images": ["array of image URLs"],
  "tags": ["array of strings"],
  "notes": "string",
  "is_favorite": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 4. Core Functionality
- **Recipe Management**:
  - Add new recipes via URL/video
  - Edit existing recipes
  - Delete recipes
  - Mark as favorite
  - Add personal notes
- **Search & Filter**:
  - Search by title, ingredients, tags
  - Filter by cuisine, dietary restrictions, cooking time
  - Sort by date, favorites, cooking time
- **Recipe View**:
  - Detailed recipe page
  - Print-friendly version
  - Share functionality
  - Cooking mode (step-by-step view)
- **Collections**:
  - Create custom recipe collections
  - Meal planning feature
  - Shopping list generation

### 5. Additional Features to Consider
- **Social Features**:
  - Share recipes with other users
  - Public/private recipes
  - Recipe ratings and reviews
  - Follow other users
- **Advanced Features**:
  - Recipe scaling (adjust servings)
  - Unit conversion
  - Ingredient substitution suggestions
  - Cooking timers
  - Export recipes (PDF, JSON)
- **AI Enhancements**:
  - Recipe recommendations
  - Meal plan suggestions
  - Nutritional analysis
  - Similar recipe suggestions

## Project Structure

### Backend (FastAPI)
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── recipes.py
│   │   └── users.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── gemini.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── recipe.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── recipe.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   ├── youtube.py
│   │   └── instagram.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── requirements.txt
├── .env.example
└── Dockerfile
```

### Frontend (Next.js)
```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── (auth)/
│   │   ├── login/
│   │   ├── register/
│   │   └── reset-password/
│   ├── dashboard/
│   │   ├── page.tsx
│   │   └── layout.tsx
│   ├── recipes/
│   │   ├── page.tsx
│   │   ├── [id]/
│   │   ├── new/
│   │   └── edit/[id]/
│   └── api/
├── components/
│   ├── ui/
│   ├── layout/
│   ├── recipes/
│   └── auth/
├── lib/
│   ├── api.ts
│   ├── auth.ts
│   └── utils.ts
├── hooks/
├── types/
├── styles/
├── public/
├── package.json
├── next.config.js
└── Dockerfile
```

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
1. Set up project structure
2. Configure MongoDB connection
3. Implement basic authentication
4. Create user registration/login
5. Set up Gemini API integration
6. Basic recipe model and CRUD API

### Phase 2: Core Features (Week 3-4)
1. Recipe URL scraping service
2. YouTube integration
3. Instagram integration (if API available)
4. Recipe data processing with Gemini
5. Frontend recipe management UI
6. Search and filter functionality

### Phase 3: Enhanced Features (Week 5-6)
1. Recipe collections
2. Favorites and notes
3. Advanced search/filters
4. Recipe editing UI
5. Responsive design polish
6. Error handling and validation

### Phase 4: Polish & Deploy (Week 7-8)
1. Testing (unit, integration)
2. Performance optimization
3. Security audit
4. Deployment setup
5. Documentation
6. User feedback implementation

## Security Considerations
- Input validation for all user inputs
- Rate limiting on API endpoints
- Secure storage of API keys
- XSS and CSRF protection
- Regular security updates
- Data encryption for sensitive info

## Performance Optimizations
- Image optimization and CDN
- Database indexing
- API response caching
- Lazy loading for recipe lists
- Pagination for large datasets
- Background job processing for scraping

## Monitoring & Analytics
- Error tracking (Sentry)
- Performance monitoring
- User analytics (privacy-friendly)
- API usage tracking
- Database performance metrics

## Future Enhancements
- Mobile app (React Native)
- Voice input for recipes
- Barcode scanning for ingredients
- Integration with grocery delivery
- Multi-language support
- Recipe video tutorials
- AI-powered meal planning