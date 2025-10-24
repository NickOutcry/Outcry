#!/usr/bin/env python3
"""
Add product variable entries to the PostgreSQL database
"""

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ProductVariable, Product

# Database connection details
DATABASE_URL = 'postgresql://postgres:gdn55L!VSpo@localhost:5432/outcry_db'

def add_product_variables():
    """Add the specified product variable entries"""
    try:
        # Create SQLAlchemy engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # First, find the product with ID 4
        product = db.query(Product).filter(Product.product_id == 3).first()
        
        if not product:
            print("❌ Error: Product with ID 5 not found in database")
            print("Available products:")
            products = db.query(Product).all()
            for prod in products:
                print(f"  - {prod.product_id}: {prod.name}")
            return
        
        print(f"✅ Found product with ID 5: {product.name}")
        
        # Product variables to add
        product_variables = [
            {
                "name": "Media",
                "base_cost": 0.00,
                "multiplier_cost": 1.0,
                "data_type": "select"
            },
            {
                "name": "Length",
                "base_cost": 0.00,
                "multiplier_cost": 1.0,
                "data_type": "number"
            },
            {
                "name": "Width",
                "base_cost": 0.00,
                "multiplier_cost": 1.0,
                "data_type": "number"
            },
            {
                "name": "Install",
                "base_cost": 15.00,
                "multiplier_cost": 1.3,
                "data_type": "select"
            },
            {
                "name": "Surface",
                "base_cost": 0.00,
                "multiplier_cost": 1.0,
                "data_type": "select"
            }
        ]
        
        # Check which ones already exist for this product
        existing_variables = db.query(ProductVariable.name).filter(ProductVariable.product_id == 5).all()
        existing_list = [variable[0] for variable in existing_variables]
        
        print(f"\nCurrent product variables for '{product.name}':")
        for variable in existing_list:
            print(f"  - {variable}")
        
        print(f"\nAdding new product variables to '{product.name}'...")
        
        # Add new variables
        added_count = 0
        for variable_data in product_variables:
            if variable_data["name"] not in existing_list:
                new_variable = ProductVariable(
                    name=variable_data["name"],
                    base_cost=variable_data["base_cost"],
                    multiplier_cost=variable_data["multiplier_cost"],
                    data_type=variable_data["data_type"],
                    product_id=5
                )
                db.add(new_variable)
                print(f"  + Adding: {variable_data['name']} (Base: ${variable_data['base_cost']}, Multiplier: {variable_data['multiplier_cost']}, Type: {variable_data['data_type']})")
                added_count += 1
            else:
                print(f"  ✓ Already exists: {variable_data['name']}")
        
        # Commit changes
        if added_count > 0:
            db.commit()
            print(f"\n✅ Successfully added {added_count} new product variable(s)")
        else:
            print(f"\nℹ️  All product variables already exist in the database")
        
        # Show final list of variables for this product
        print(f"\nProduct variables for '{product.name}':")
        product_vars = db.query(ProductVariable).filter(ProductVariable.product_id == 5).all()
        for variable in product_vars:
            print(f"  - {variable.name} (Base: ${variable.base_cost}, Multiplier: {variable.multiplier_cost}, Type: {variable.data_type})")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()

if __name__ == "__main__":
    print("=== Adding Product Variables to Database ===")
    print()
    add_product_variables()