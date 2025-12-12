#!/bin/bash

# Outcry Projects - FastAPI Server Startup Script
# This script creates a virtual environment, installs dependencies, and runs the server

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
MAIN_FILE="main.py"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5001}"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Python 3 is available
check_python() {
    print_info "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Found $PYTHON_VERSION"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version)
        if [[ $PYTHON_VERSION == *"Python 3"* ]]; then
            print_success "Found $PYTHON_VERSION"
            PYTHON_CMD="python"
        else
            print_error "Python 3 is required but only Python 2 was found"
            exit 1
        fi
    else
        print_error "Python 3 is not installed. Please install Python 3.7 or higher."
        exit 1
    fi
}

# Create virtual environment if it doesn't exist
create_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_info "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        print_success "Virtual environment created in $VENV_DIR/"
    else
        print_info "Virtual environment already exists in $VENV_DIR/"
    fi
}

# Activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        print_success "Virtual environment activated"
    elif [ -f "$VENV_DIR/Scripts/activate" ]; then
        source "$VENV_DIR/Scripts/activate"
        print_success "Virtual environment activated (Windows)"
    else
        print_error "Could not find virtual environment activation script"
        exit 1
    fi
}

# Upgrade pip
upgrade_pip() {
    print_info "Upgrading pip..."
    pip install --upgrade pip --quiet
    print_success "pip upgraded"
}

# Install dependencies
install_dependencies() {
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        print_error "Requirements file $REQUIREMENTS_FILE not found!"
        exit 1
    fi
    
    print_info "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
    print_success "Dependencies installed"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating template .env file..."
        cat > .env << EOF
# Database Configuration
DATABASE_URL=sqlite:///outcry_database.db

# Dropbox Configuration (optional)
# DROPBOX_ACCESS_TOKEN=your_dropbox_token_here

# Google Maps API Key (optional)
# GOOGLE_MAPS_API_KEY=your_google_maps_key_here

# Application Configuration
APP_NAME=Outcry Projects API
APP_VERSION=2.0.0
DEBUG=False
HOST=0.0.0.0
PORT=5001

# CORS Configuration
CORS_ORIGINS=*
CORS_ALLOW_CREDENTIALS=True
EOF
        print_success "Template .env file created. Please update it with your configuration."
    else
        print_info ".env file found"
    fi
}

# Run the FastAPI server
run_server() {
    if [ ! -f "$MAIN_FILE" ]; then
        print_error "Main file $MAIN_FILE not found!"
        exit 1
    fi
    
    print_info "Starting FastAPI server..."
    print_info "Server will be available at http://$HOST:$PORT"
    print_info "API Documentation: http://$HOST:$PORT/docs"
    print_info "Press Ctrl+C to stop the server"
    echo ""
    
    uvicorn main:app --host "$HOST" --port "$PORT" --reload
}

# Main execution
main() {
    echo "=========================================="
    echo "  Outcry Projects - FastAPI Server"
    echo "=========================================="
    echo ""
    
    # Check Python
    check_python
    
    # Create virtual environment
    create_venv
    
    # Activate virtual environment
    activate_venv
    
    # Upgrade pip
    upgrade_pip
    
    # Install dependencies
    install_dependencies
    
    # Check .env file
    check_env_file
    
    echo ""
    print_success "Setup complete!"
    echo ""
    
    # Run server
    run_server
}

# Run main function
main

