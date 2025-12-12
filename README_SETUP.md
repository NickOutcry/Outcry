# Setup and Run Guide

## Quick Start

### Using the Setup Script (Recommended)

Simply run the provided shell script:

```bash
./run.sh
```

This script will:
1. Check for Python 3 installation
2. Create a virtual environment (if it doesn't exist)
3. Install all dependencies from `requirements.txt`
4. Create a template `.env` file (if it doesn't exist)
5. Start the FastAPI server with uvicorn

### Manual Setup

If you prefer to set up manually:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file (copy from .env.example if available)
# Edit .env with your configuration

# 6. Run the server
uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/outcry_db
# Or for SQLite:
# DATABASE_URL=sqlite:///outcry_database.db

# Dropbox Configuration (optional)
DROPBOX_ACCESS_TOKEN=your_dropbox_token_here

# Google Maps API Key (optional)
GOOGLE_MAPS_API_KEY=your_google_maps_key_here

# Application Configuration
APP_NAME=Outcry Projects API
APP_VERSION=2.0.0
DEBUG=False
HOST=0.0.0.0
PORT=5001

# CORS Configuration
CORS_ORIGINS=*
CORS_ALLOW_CREDENTIALS=True
```

## Running the Server

### Development Mode (with auto-reload)
```bash
uvicorn main:app --reload
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 5001
```

### Using the Script
```bash
./run.sh
```

## Accessing the API

Once the server is running:

- **API Root**: http://localhost:5001/
- **API Documentation (Swagger)**: http://localhost:5001/docs
- **API Documentation (ReDoc)**: http://localhost:5001/redoc
- **Health Check**: http://localhost:5001/health
- **API Info**: http://localhost:5001/api/info

## Troubleshooting

### Virtual Environment Issues
If you encounter issues with the virtual environment:
```bash
# Remove existing venv
rm -rf venv

# Recreate it
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
If port 5001 is already in use, you can change it:
```bash
# Set PORT environment variable
export PORT=5002
./run.sh

# Or specify directly
uvicorn main:app --port 5002
```

### Database Connection Issues
Make sure your `DATABASE_URL` in `.env` is correct and the database server is running.

### Dropbox Issues
If Dropbox is not configured, the application will still run but file upload features will be disabled.

