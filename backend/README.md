# Smart Recipe Keeper Backend

## Setup with uv

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

## MongoDB Setup

1. Install MongoDB locally or use MongoDB Atlas
2. Update `MONGODB_URL` in `.env`

## API Documentation

Once running, visit:
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

## Testing

```bash
pytest
```

## Code Formatting

```bash
black .
flake8
mypy .
```