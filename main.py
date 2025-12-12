"""
FastAPI Application Entry Point
Main entry point for the Outcry Projects API
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import configuration
from config import (
    DROPBOX_AVAILABLE,
    DROPBOX_ACCESS_TOKEN,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS,
    APP_NAME,
    APP_VERSION,
    HOST,
    PORT
)

# Import routers
from routers import (
    client_router,
    delivery_router,
    job_router,
    product_router,
    public_router,
    staff_router,
    throughput_router,
    upload_router,  # File upload router
)

# Try to import dropbox_service, but make it optional
try:
    from dropbox_service import initialize_dropbox_service
except ImportError:
    print("Warning: dropbox_service not available")

# Create FastAPI application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Outcry Projects API - FastAPI backend for project management",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - Fully open for React frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Note: Static files and templates removed - this is an API-only backend
# Static files for uploads are handled via Dropbox integration

# Initialize Dropbox service (if available)
if DROPBOX_AVAILABLE and DROPBOX_ACCESS_TOKEN:
    try:
        initialize_dropbox_service(DROPBOX_ACCESS_TOKEN)
        print("✓ Dropbox service initialized successfully")
    except Exception as e:
        print(f"⚠ Warning: Failed to initialize Dropbox service: {str(e)}")
elif DROPBOX_AVAILABLE:
    print("⚠ Warning: DROPBOX_ACCESS_TOKEN not found in environment variables")

# Include routers - All domain routers
app.include_router(client_router)      # Client domain: Client, Contact, Billing
app.include_router(delivery_router)   # Delivery domain: Address, Booking, Attachment
app.include_router(job_router)        # Job domain: Project, Quote, Job, Item, etc.
app.include_router(product_router)     # Product domain: Product, Category, Variable, etc.
app.include_router(public_router)      # Public schema: General/system tables
app.include_router(staff_router)      # Staff domain: Staff
app.include_router(throughput_router)  # Throughput domain: Status, Stage, Task, StageDate
app.include_router(upload_router)      # File upload: Dropbox integration

# Root endpoint
@app.get("/", response_class=JSONResponse)
async def root():
    """
    Root endpoint - Returns API information
    """
    return {
        "message": "Welcome to Outcry Projects API",
        "name": APP_NAME,
        "version": APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running"
    }

# Health check endpoint
@app.get("/health", response_class=JSONResponse)
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION
    }

# API info endpoint
@app.get("/api/info", response_class=JSONResponse)
async def api_info():
    """
    API information endpoint
    """
    from config import get_config_summary
    
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        },
        "configuration": get_config_summary()
    }

# Google Maps API key endpoint (if needed by frontend)
@app.get("/api/google-maps-key", response_class=JSONResponse)
async def get_google_maps_key():
    """
    Return Google Maps API key for client-side use
    """
    from config import GOOGLE_MAPS_API_KEY
    return {"apiKey": GOOGLE_MAPS_API_KEY}


if __name__ == "__main__":
    import uvicorn
    
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    print(f"Server running on http://{HOST}:{PORT}")
    print(f"API Documentation available at http://{HOST}:{PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True
    )

