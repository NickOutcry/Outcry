# Outcry Projects - Complete Setup Guide

This guide will help you set up and run both the FastAPI backend and React frontend.

## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 18+** and **npm** (for frontend)
- **PostgreSQL** (or SQLite for development)
- **Git** (optional)

## Backend Setup (FastAPI)

### 1. Navigate to Project Root

```bash
cd /Users/nicholasnolan/Desktop/Outcry_Projects
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/outcry_db
DB_POOL_SIZE=10
DB_ECHO=False

# Dropbox (optional)
DROPBOX_ACCESS_TOKEN=your_dropbox_token_here
DROPBOX_BASE_PATH=/Outcry_Projects

# API Keys
GOOGLE_MAPS_API_KEY=your_google_maps_key_here

# Application
APP_NAME=Outcry Projects API
APP_VERSION=2.0.0
DEBUG=False
HOST=0.0.0.0
PORT=5001

# CORS (fully open for development)
CORS_ORIGINS=*
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*

# File Upload
MAX_UPLOAD_SIZE=104857600  # 100 MB
ALLOWED_EXTENSIONS=pdf,doc,docx,xls,xlsx,jpg,jpeg,png,gif,zip

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Logging
LOG_LEVEL=INFO
```

### 5. Run Backend

**Option 1: Using the startup script (recommended)**
```bash
./run.sh
```

**Option 2: Using uvicorn directly**
```bash
uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

**Option 3: Using Python**
```bash
python main.py
```

The backend will be available at: **http://localhost:5001**

- **API Documentation**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc
- **Health Check**: http://localhost:5001/health

## Frontend Setup (React)

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

This will install:
- React 18
- Vite
- Tailwind CSS
- React Router DOM
- Axios
- Tailwind plugins (forms, typography)

### 3. Configure Environment (Optional)

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:5001/api
```

**Note**: In development, Vite's proxy handles `/api` requests automatically. This is only needed for production builds.

### 4. Run Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

### 5. Build for Production

```bash
npm run build
```

The production build will be in `frontend/dist/`.

### 6. Preview Production Build

```bash
npm run preview
```

## Running Both Servers

### Terminal 1: Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Run backend
uvicorn main:app --reload
```

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

## Project Structure

```
Outcry_Projects/
├── main.py                 # FastAPI entry point
├── config.py               # Configuration
├── database.py             # Database setup
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── run.sh                  # Backend startup script
│
├── models/                 # SQLAlchemy models
│   ├── client.py
│   ├── product.py
│   ├── job.py
│   ├── staff.py
│   ├── delivery.py
│   ├── throughput.py
│   └── public.py
│
├── schemas/                # Pydantic schemas
│   ├── client.py
│   ├── product.py
│   ├── job.py
│   ├── staff.py
│   ├── delivery.py
│   ├── throughput.py
│   └── public.py
│
├── routers/                # FastAPI routers
│   ├── client.py
│   ├── product.py
│   ├── job.py
│   ├── staff.py
│   ├── delivery.py
│   ├── throughput.py
│   ├── public.py
│   └── upload.py
│
└── frontend/               # React frontend
    ├── src/
    │   ├── components/     # React components
    │   │   ├── Button.jsx
    │   │   ├── Input.jsx
    │   │   └── Card.jsx
    │   ├── pages/          # Page components
    │   │   ├── Dashboard.jsx
    │   │   ├── Projects.jsx
    │   │   ├── Jobs.jsx
    │   │   ├── Products.jsx
    │   │   └── Staff.jsx
    │   ├── styles/         # CSS and design tokens
    │   │   ├── tokens.css
    │   │   └── globals.css
    │   ├── api/            # API clients
    │   │   ├── index.js
    │   │   ├── client.js
    │   │   ├── job.js
    │   │   ├── product.js
    │   │   └── staff.js
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── postcss.config.js
```

## Testing

### Backend Test Endpoints

Test database connections for each domain:

```bash
# Client domain
curl http://localhost:5001/api/client/test

# Staff domain
curl http://localhost:5001/api/staff/test

# Product domain
curl http://localhost:5001/api/product/test

# Job domain
curl http://localhost:5001/api/job/test

# Delivery domain
curl http://localhost:5001/api/delivery/test

# Throughput domain
curl http://localhost:5001/api/throughput/test

# Public schema
curl http://localhost:5001/api/public/test
```

### Frontend API Integration

The frontend is configured to proxy API requests to the backend during development. All API calls go through `/api` which is proxied to `http://localhost:5001/api`.

## Design System

The frontend uses a design token system defined in `frontend/src/styles/tokens.css`. All design values (colors, spacing, shadows, etc.) are mapped to Tailwind CSS through `tailwind.config.js`.

### Using Design Tokens

```jsx
// Colors
<div className="bg-primary text-white">Primary</div>
<div className="bg-neutral-100">Light Background</div>

// Spacing
<div className="p-4 m-6">Padding and Margin</div>

// Border Radius
<button className="rounded-md">Rounded Button</button>
```

## Troubleshooting

### Backend Issues

**Database Connection Error**
- Check `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running
- Verify database credentials

**Import Errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Port Already in Use**
- Change `PORT` in `.env` or use `--port` flag
- Kill the process using port 5001: `lsof -ti:5001 | xargs kill`

### Frontend Issues

**API Connection Errors**
- Verify backend is running on port 5001
- Check browser console for CORS errors
- Ensure `VITE_API_URL` is set correctly in `.env`

**Build Errors**
- Run `npm install` to ensure all dependencies are installed
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`

**Tailwind Not Working**
- Ensure `tokens.css` is imported in `globals.css`
- Check `tailwind.config.js` content paths
- Restart the dev server

### CORS Issues

The backend CORS is fully open for development (`allow_origins=["*"]`). If you encounter CORS errors:

1. Check that the backend is running
2. Verify CORS middleware is configured in `main.py`
3. Check browser console for specific error messages

## Production Deployment

### Backend

1. Set production environment variables
2. Restrict CORS origins in `config.py` (change `CORS_ORIGINS` from `*` to specific domains)
3. Use production ASGI server:

```bash
pip install gunicorn
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

**Example nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Serve frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests
    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Next Steps

1. **Explore the API**: Visit http://localhost:5001/docs to see all available endpoints
2. **Build Components**: Start building UI components using the design tokens
3. **Integrate APIs**: Connect frontend pages to backend APIs
4. **Add Authentication**: Implement user authentication and authorization
5. **Deploy**: Deploy both backend and frontend to production

## Additional Resources

- **Backend API Documentation**: See `README_FASTAPI.md`
- **Frontend Documentation**: See `frontend/README.md`
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Tailwind CSS Docs**: https://tailwindcss.com/
- **Vite Docs**: https://vitejs.dev/
