"""
Configuration module for Outcry Projects
Loads environment variables from .env and provides constants
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# Database URL - defaults to SQLite if not provided
DATABASE_URL: str = os.getenv(
    'DATABASE_URL',
    'sqlite:///outcry_database.db'
)

# Database connection pool settings
DB_POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE', '5'))
DB_MAX_OVERFLOW: int = int(os.getenv('DB_MAX_OVERFLOW', '10'))
DB_POOL_RECYCLE: int = int(os.getenv('DB_POOL_RECYCLE', '3600'))

# Enable SQLAlchemy echo (SQL query logging)
DB_ECHO: bool = os.getenv('DB_ECHO', 'False').lower() == 'true'


# ============================================================================
# DROPBOX CONFIGURATION
# ============================================================================

# Dropbox access token
DROPBOX_ACCESS_TOKEN: Optional[str] = os.getenv('DROPBOX_ACCESS_TOKEN')

# Check if Dropbox is available
DROPBOX_AVAILABLE: bool = DROPBOX_ACCESS_TOKEN is not None

# Dropbox base path for uploads
DROPBOX_BASE_PATH: str = os.getenv('DROPBOX_BASE_PATH', '/Outcry_Projects')


# ============================================================================
# API KEYS
# ============================================================================

# Google Maps API key
GOOGLE_MAPS_API_KEY: str = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY')


# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

# Application settings
APP_NAME: str = os.getenv('APP_NAME', 'Outcry Projects API')
APP_VERSION: str = os.getenv('APP_VERSION', '2.0.0')
DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'

# Server settings
HOST: str = os.getenv('HOST', '0.0.0.0')
PORT: int = int(os.getenv('PORT', '5001'))

# CORS settings
CORS_ORIGINS: list = os.getenv(
    'CORS_ORIGINS',
    '*'
).split(',') if os.getenv('CORS_ORIGINS') != '*' else ['*']

CORS_ALLOW_CREDENTIALS: bool = os.getenv(
    'CORS_ALLOW_CREDENTIALS',
    'True'
).lower() == 'true'

CORS_ALLOW_METHODS: list = os.getenv(
    'CORS_ALLOW_METHODS',
    '*'
).split(',') if os.getenv('CORS_ALLOW_METHODS') != '*' else ['*']

CORS_ALLOW_HEADERS: list = os.getenv(
    'CORS_ALLOW_HEADERS',
    '*'
).split(',') if os.getenv('CORS_ALLOW_HEADERS') != '*' else ['*']


# ============================================================================
# FILE UPLOAD CONFIGURATION
# ============================================================================

# Maximum file size in bytes (default: 100MB)
MAX_UPLOAD_SIZE: int = int(os.getenv('MAX_UPLOAD_SIZE', str(100 * 1024 * 1024)))

# Allowed file extensions
ALLOWED_EXTENSIONS: list = os.getenv(
    'ALLOWED_EXTENSIONS',
    'pdf,doc,docx,xls,xlsx,jpg,jpeg,png,gif,zip'
).split(',')


# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

# Secret key for session management (if needed)
SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# JWT settings (if using authentication)
JWT_SECRET_KEY: Optional[str] = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_HOURS: int = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log level
LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

# Log file path
LOG_FILE: Optional[str] = os.getenv('LOG_FILE')


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_config():
    """
    Validate that required configuration values are set
    Raises ValueError if required values are missing
    """
    errors = []
    
    # Check database URL
    if not DATABASE_URL:
        errors.append("DATABASE_URL is required")
    
    # Check Dropbox token if Dropbox is expected to be used
    if DROPBOX_AVAILABLE and not DROPBOX_ACCESS_TOKEN:
        errors.append("DROPBOX_ACCESS_TOKEN is required when using Dropbox")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True


def get_config_summary() -> dict:
    """
    Get a summary of current configuration (without sensitive data)
    """
    return {
        "database": {
            "url": DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL,
            "pool_size": DB_POOL_SIZE,
            "echo": DB_ECHO
        },
        "dropbox": {
            "available": DROPBOX_AVAILABLE,
            "base_path": DROPBOX_BASE_PATH
        },
        "app": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "debug": DEBUG,
            "host": HOST,
            "port": PORT
        },
        "cors": {
            "origins": CORS_ORIGINS if len(CORS_ORIGINS) < 5 else f"{len(CORS_ORIGINS)} origins",
            "allow_credentials": CORS_ALLOW_CREDENTIALS
        },
        "upload": {
            "max_size_mb": MAX_UPLOAD_SIZE / (1024 * 1024),
            "allowed_extensions": ALLOWED_EXTENSIONS
        }
    }


# Validate configuration on import
try:
    validate_config()
except ValueError as e:
    print(f"Warning: {e}")

