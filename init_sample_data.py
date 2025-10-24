from database import SessionLocal, create_tables
from models import ProductCategory, Product, ProductVariable, VariableOption

def init_sample_data():
    """Initialize the database with sample data"""
    db = SessionLocal()
    
    try:
        # Create sample categories
        categories = [
            ProductCategory(name="Signage"),
            ProductCategory(name="Printing"),
            ProductCategory(name="Digital")
        ]
        
        for category in categories:
            db.add(category)
        db.commit()
        
        # Refresh to get IDs
        for category in categories:
            db.refresh(category)
        
        # Create sample products
        products = [
            Product(
                name="Vinyl Banner",
                base_cost=25.00,
                multiplier_cost=0.15,
                product_category_id=categories[0].product_category_id
            ),
            Product(
                name="Business Cards",
                base_cost=50.00,
                multiplier_cost=0.05,
                product_category_id=categories[1].product_category_id
            ),
            Product(
                name="Website Design",
                base_cost=500.00,
                multiplier_cost=0.00,
                product_category_id=categories[2].product_category_id
            )
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        
        # Refresh to get IDs
        for product in products:
            db.refresh(product)
        
        # Create sample variables
        variables = [
            # Vinyl Banner variables
            ProductVariable(
                name="Size",
                base_cost=0.00,
                multiplier_cost=0.10,
                data_type="select",
                product_id=products[0].product_id
            ),
            ProductVariable(
                name="Material",
                base_cost=0.00,
                multiplier_cost=0.20,
                data_type="select",
                product_id=products[0].product_id
            ),
            # Business Cards variables
            ProductVariable(
                name="Quantity",
                base_cost=0.00,
                multiplier_cost=0.02,
                data_type="number",
                product_id=products[1].product_id
            ),
            ProductVariable(
                name="Finish",
                base_cost=0.00,
                multiplier_cost=0.10,
                data_type="select",
                product_id=products[1].product_id
            ),
            # Website Design variables
            ProductVariable(
                name="Pages",
                base_cost=0.00,
                multiplier_cost=50.00,
                data_type="number",
                product_id=products[2].product_id
            ),
            ProductVariable(
                name="Features",
                base_cost=0.00,
                multiplier_cost=0.00,
                data_type="select",
                product_id=products[2].product_id
            )
        ]
        
        for variable in variables:
            db.add(variable)
        db.commit()
        
        # Refresh to get IDs
        for variable in variables:
            db.refresh(variable)
        
        # Create sample options
        options = [
            # Size options for Vinyl Banner
            VariableOption(
                name="Small (1m x 1m)",
                base_cost=0.00,
                multiplier_cost=0.05,
                product_variable_id=variables[0].product_variable_id
            ),
            VariableOption(
                name="Medium (2m x 1m)",
                base_cost=5.00,
                multiplier_cost=0.10,
                product_variable_id=variables[0].product_variable_id
            ),
            VariableOption(
                name="Large (3m x 1m)",
                base_cost=10.00,
                multiplier_cost=0.15,
                product_variable_id=variables[0].product_variable_id
            ),
            # Material options for Vinyl Banner
            VariableOption(
                name="Standard Vinyl",
                base_cost=0.00,
                multiplier_cost=0.15,
                product_variable_id=variables[1].product_variable_id
            ),
            VariableOption(
                name="Premium Vinyl",
                base_cost=15.00,
                multiplier_cost=0.25,
                product_variable_id=variables[1].product_variable_id
            ),
            VariableOption(
                name="Mesh Vinyl",
                base_cost=20.00,
                multiplier_cost=0.30,
                product_variable_id=variables[1].product_variable_id
            ),
            # Finish options for Business Cards
            VariableOption(
                name="Standard",
                base_cost=0.00,
                multiplier_cost=0.05,
                product_variable_id=variables[3].product_variable_id
            ),
            VariableOption(
                name="Gloss",
                base_cost=10.00,
                multiplier_cost=0.15,
                product_variable_id=variables[3].product_variable_id
            ),
            VariableOption(
                name="Matte",
                base_cost=15.00,
                multiplier_cost=0.20,
                product_variable_id=variables[3].product_variable_id
            ),
            # Features options for Website Design
            VariableOption(
                name="Basic",
                base_cost=0.00,
                multiplier_cost=0.00,
                product_variable_id=variables[5].product_variable_id
            ),
            VariableOption(
                name="E-commerce",
                base_cost=200.00,
                multiplier_cost=0.00,
                product_variable_id=variables[5].product_variable_id
            ),
            VariableOption(
                name="CMS",
                base_cost=150.00,
                multiplier_cost=0.00,
                product_variable_id=variables[5].product_variable_id
            )
        ]
        
        for option in options:
            db.add(option)
        db.commit()
        
        print("Sample data initialized successfully!")
        print(f"Created {len(categories)} categories")
        print(f"Created {len(products)} products")
        print(f"Created {len(variables)} variables")
        print(f"Created {len(options)} options")
        
    except Exception as e:
        db.rollback()
        print(f"Error initializing sample data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables first
    create_tables()
    print("Database tables created!")
    
    # Initialize sample data
    init_sample_data()

