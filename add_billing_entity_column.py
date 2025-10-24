#!/usr/bin/env python3

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("Error: DATABASE_URL not found in environment variables")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

def add_billing_entity_column():
    """Add billing_entity column to job.jobs table if it doesn't exist"""
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'job' 
                AND table_name = 'jobs' 
                AND column_name = 'billing_entity'
            """))
            
            if result.fetchone():
                print("Column 'billing_entity' already exists in job.jobs table")
                return
            
            # Add the column
            conn.execute(text("""
                ALTER TABLE job.jobs 
                ADD COLUMN billing_entity INTEGER REFERENCES client.billing(billing_id)
            """))
            conn.commit()
            print("Successfully added 'billing_entity' column to job.jobs table")
            
    except Exception as e:
        print(f"Error adding billing_entity column: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_billing_entity_column()

