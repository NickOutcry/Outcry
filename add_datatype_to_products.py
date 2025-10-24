from database import engine
from sqlalchemy import text

print('Adding datatype foreign key column to products table...')
try:
    with engine.connect() as conn:
        # Add the datatype column as a foreign key
        conn.execute(text("""
            ALTER TABLE products 
            ADD COLUMN datatype_id INTEGER REFERENCES datatype(datatype_id)
        """))
        conn.commit()
        print('✅ Datatype column added successfully!')
        
        # Verify the column was added
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'products' AND column_name = 'datatype_id'
        """))
        
        if result.fetchone():
            print('✅ Column verification successful!')
            
            # Show updated products table structure
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'products' 
                ORDER BY ordinal_position
            """))
            print('\nUpdated products table structure:')
            for row in result:
                print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
                
            # Check foreign key constraint
            result = conn.execute(text("""
                SELECT 
                    tc.constraint_name,
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_name = 'products' 
                AND kcu.column_name = 'datatype_id'
            """))
            
            print('\nForeign key constraints:')
            for row in result:
                print(f'  {row[0]}: {row[1]}.{row[2]} -> {row[3]}.{row[4]}')
        else:
            print('❌ Column addition failed!')
            
except Exception as e:
    print('❌ Error adding column:', e)

