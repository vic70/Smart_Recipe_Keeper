# Smart Recipe Keeper

A full-stack application for saving and organizing recipes from various sources including websites, YouTube videos, and Instagram reels using AI-powered content extraction.

## Features

- 🔗 Extract recipes from any website URL
- 📹 Support for YouTube and Instagram content (coming soon)
- 🤖 AI-powered recipe extraction using Google Gemini
- 👤 User authentication and personal recipe collections
- 🏷️ Tag and categorize recipes by food nature (appetizer, main course, dessert, etc.)
- 🔍 Search and filter functionality
- 📱 Responsive design for all devices

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI (Python), MongoDB, Beanie ODM
- **AI**: Google Gemini API
- **Authentication**: JWT tokens

## Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB (local or Atlas)
- Google Gemini API key

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/vic70/Smart_Recipe_Keeper.git
cd Smart_Recipe_Keeper
```

### 2. Set up the Backend

```bash
cd backend

# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration (MongoDB URL, Gemini API key, etc.)

# Run the backend server
uvicorn app.main:app --reload
```

The backend will be available at http://localhost:8000

### 3. Set up the Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local if needed

# Run the development server
npm run dev
```

The frontend will be available at http://localhost:3000

## Environment Variables

### Backend (.env)
- `MONGODB_URL`: MongoDB connection string
- `SECRET_KEY`: JWT secret key (generate a secure random string)
- `GEMINI_API_KEY`: Your Google Gemini API key

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000/api/v1)

## API Documentation

Once the backend is running, visit:
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

## Project Structure

```
Smart_Recipe_Keeper/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality (auth, security)
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic (extractors, AI)
│   └── pyproject.toml    # Python dependencies
├── frontend/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/              # Utilities and API client
│   └── package.json      # Node dependencies
└── PROJECT_PLAN.md       # Detailed project plan
```

## Development Workflow

1. Backend API runs on port 8000
2. Frontend runs on port 3000
3. MongoDB should be running (local or Atlas)
4. Add your Gemini API key to use AI features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.