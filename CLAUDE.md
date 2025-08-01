# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Smart Recipe Keeper - A full-stack recipe management application that extracts recipes from URLs (websites, YouTube, Instagram) using AI.

## Tech Stack

- **Backend**: Python FastAPI with MongoDB
- **Frontend**: Next.js 14+ with TypeScript, shadcn/ui, Tailwind CSS
- **AI**: Google Gemini API for content extraction
- **Database**: MongoDB with Beanie ODM
- **Authentication**: JWT tokens

## Development Commands

### Backend (using uv)
```bash
cd backend
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Run development server
uvicorn app.main:app --reload  # Runs on http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

## Project Structure

### Backend Architecture
- **Modular Extractors**: Base class system for extensible content extraction
- **Services**: Separated concerns (extractors, Gemini integration)
- **API Structure**: RESTful endpoints under `/api/v1`
- **Authentication**: JWT with access/refresh tokens
- **Models**: MongoDB documents using Beanie ODM

### Key Patterns
1. **Factory Pattern**: ExtractorFactory for URL type detection
2. **Dependency Injection**: FastAPI's Depends for auth/DB
3. **Async/Await**: Throughout for non-blocking operations
4. **Rate Limiting**: Implemented on auth endpoints

## Environment Variables

Backend requires:
- `MONGODB_URL`: MongoDB connection string
- `SECRET_KEY`: JWT secret key
- `GEMINI_API_KEY`: Google Gemini API key

Frontend requires:
- `NEXT_PUBLIC_API_URL`: Backend API URL

## API Endpoints

- POST `/api/v1/auth/register` - User registration
- POST `/api/v1/auth/login` - User login
- POST `/api/v1/recipes/extract` - Extract recipe from URL
- GET `/api/v1/recipes` - List user recipes
- PUT `/api/v1/recipes/{id}` - Update recipe
- DELETE `/api/v1/recipes/{id}` - Delete recipe

## Notes

- Repository URL: https://github.com/vic70/Smart_Recipe_Keeper.git
- Backend API runs on port 8000
- Frontend runs on port 3000
- CORS configured for local development

## Environment Files

- `.env.example` files are templates and are committed to the repository
- `.env` (backend) and `.env.local` (frontend) are gitignored and contain actual secrets
- Always use `.env.example` as a template when setting up a new environment