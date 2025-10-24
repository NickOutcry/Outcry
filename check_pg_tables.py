from database import engine
from sqlalchemy import text

print('Checking PostgreSQL database tables...')
try:
    with engine.connect() as conn:
        # Check if tables exist
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('product_categories', 'products', 'product_variables', 'variable_options')
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        print('Existing tables:', tables)
        
        if 'product_categories' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM product_categories"))
            count = result.fetchone()[0]
            print(f'Product categories count: {count}')
            
            if count > 0:
                result = conn.execute(text("SELECT * FROM product_categories LIMIT 5"))
                categories = result.fetchall()
                print('Sample categories:', categories)
        
        if 'products' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM products"))
            count = result.fetchone()[0]
            print(f'Products count: {count}')
            
            if count > 0:
                result = conn.execute(text("SELECT * FROM products LIMIT 5"))
                products = result.fetchall()
                print('Sample products:', products)
                
except Exception as e:
    print('Error:', e)

