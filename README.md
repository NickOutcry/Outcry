# Outcry Projects

Full-stack project management application with FastAPI backend and React frontend.

## Project Structure

```
Outcry_Projects/
├── backend/              # FastAPI backend (current root)
│   ├── main.py          # FastAPI entry point
│   ├── config.py        # Configuration
│   ├── database.py     # Database setup
│   ├── models/         # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routers/         # API routers
│   └── requirements.txt
└── frontend/            # React frontend
    ├── src/
    ├── package.json
    └── vite.config.js
```

## Quick Start

### Backend Setup

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
Create a `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/outcry_db
DROPBOX_ACCESS_TOKEN=your_token_here
GOOGLE_MAPS_API_KEY=your_key_here
HOST=0.0.0.0
PORT=5001
```

4. **Run backend:**
```bash
# Option 1: Using the script
./run.sh

# Option 2: Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 5001 --reload

# Option 3: Using Python
python main.py
```

Backend will be available at: http://localhost:5001

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment (optional):**
Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:5001/api
```

4. **Run development server:**
```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

## Development Commands

### Backend

```bash
# Run with auto-reload
uvicorn main:app --reload

# Run on custom port
uvicorn main:app --port 5002
```

### Frontend

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## API Documentation

- **Swagger UI**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc

## Architecture

### Backend (FastAPI)

- **API-only**: No HTML templates or static file serving
- **Modular**: Organized by domain schemas (client, product, job, staff, delivery, throughput, public)
- **RESTful**: Full CRUD operations for all models
- **CORS**: Fully open for React frontend development

### Frontend (React + Vite + Tailwind)

- **Modern Stack**: Vite for fast development, React 18, Tailwind CSS
- **Design System**: CSS variables for design tokens
- **API Integration**: Axios-based API clients organized by domain
- **Component-based**: Reusable components (Button, Input, Card)

## Testing

### Backend Test Endpoints

Test database connections:
```bash
curl http://localhost:5001/api/client/test
curl http://localhost:5001/api/staff/test
curl http://localhost:5001/api/product/test
curl http://localhost:5001/api/job/test
curl http://localhost:5001/api/delivery/test
curl http://localhost:5001/api/throughput/test
```

### Frontend

The frontend is configured to proxy API requests to the backend during development.

## Production Deployment

### Backend

1. Set production environment variables
2. Restrict CORS origins in `config.py`
3. Use production ASGI server (e.g., Gunicorn with Uvicorn workers)

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5001
```

### Frontend

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Serve the `dist/` directory with a web server (nginx, Apache, etc.)

3. Configure the web server to proxy API requests to the backend

## Troubleshooting

### Backend Issues

- **Database connection**: Check `DATABASE_URL` in `.env`
- **Import errors**: Ensure virtual environment is activated
- **Port conflicts**: Change `PORT` in `.env` or use `--port` flag

### Frontend Issues

- **API connection**: Verify backend is running on port 5001
- **Build errors**: Run `npm install` to ensure all dependencies are installed
- **CORS errors**: Ensure backend CORS is configured to allow frontend origin

## Additional Documentation

- **Backend API**: See `README_FASTAPI.md`
- **Setup Guide**: See `README_SETUP.md`
- **Frontend**: See `frontend/README.md`
# Outcry
