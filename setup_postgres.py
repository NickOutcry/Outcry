#!/usr/bin/env python3
"""
PostgreSQL Database Setup Script
This script helps set up the outcry_db database in PostgreSQL
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database import init_database
from init_db import create_sample_data

def create_database():
    """Create the outcry_db database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="gdn55L!VSpo"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'outcry_db'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creating database 'outcry_db'...")
            cursor.execute("CREATE DATABASE outcry_db")
            print("Database 'outcry_db' created successfully!")
        else:
            print("Database 'outcry_db' already exists.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is running on localhost:5432")
        print("2. User 'postgres' exists with the correct password")
        print("3. You have permission to create databases")
        return False
    
    return True

def setup_environment():
    """Set up environment variables for PostgreSQL"""
    os.environ['DATABASE_URL'] = 'postgresql://postgres:gdn55L!VSpo@localhost:5432/outcry_db'
    print("Environment configured for PostgreSQL database.")

def main():
    """Main setup function"""
    print("=== Outcry Database PostgreSQL Setup ===")
    print()
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        return
    
    # Step 2: Set up environment
    print("\nStep 2: Configuring environment...")
    setup_environment()
    
    # Step 3: Create tables
    print("\nStep 3: Creating database tables...")
    try:
        init_database()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        return
    
    # Step 4: Ask about sample data
    print("\nStep 4: Sample data...")
    response = input("Do you want to create sample data? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        try:
            create_sample_data()
            print("Sample data created successfully!")
        except Exception as e:
            print(f"Error creating sample data: {e}")
    
    print("\n=== Setup Complete ===")
    print("Your PostgreSQL database 'outcry_db' is ready!")
    print("Connection details:")
    print("  Host: localhost")
    print("  Port: 5432")
    print("  Database: outcry_db")
    print("  Username: postgres")
    print("  Password: gdn55L!VSpo")

if __name__ == "__main__":
    main()

