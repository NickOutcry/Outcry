from database import engine
from sqlalchemy import text

print('Checking PostgreSQL table schemas...')
try:
    with engine.connect() as conn:
        # Check products table schema
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'products' 
            ORDER BY ordinal_position
        """))
        print('Products table columns:')
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
        
        print('\nProduct categories table columns:')
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'product_categories' 
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
            
        print('\nProduct variables table columns:')
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'product_variables' 
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
            
        print('\nVariable options table columns:')
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'variable_options' 
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
                
except Exception as e:
    print('Error:', e)

