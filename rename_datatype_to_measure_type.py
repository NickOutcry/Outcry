from database import engine
from sqlalchemy import text

print('Renaming datatype table to measure_type and updating columns...')
try:
    with engine.connect() as conn:
        # Step 1: Rename the table
        conn.execute(text("ALTER TABLE datatype RENAME TO measure_type"))
        print('✅ Table renamed from datatype to measure_type')
        
        # Step 2: Rename the primary key column
        conn.execute(text("ALTER TABLE measure_type RENAME COLUMN datatype_id TO measure_type_id"))
        print('✅ Primary key column renamed from datatype_id to measure_type_id')
        
        # Step 3: Rename the data column
        conn.execute(text("ALTER TABLE measure_type RENAME COLUMN datatype TO measure_type"))
        print('✅ Data column renamed from datatype to measure_type')
        
        # Step 4: Drop the existing foreign key constraint
        conn.execute(text("ALTER TABLE products DROP CONSTRAINT IF EXISTS products_datatype_id_fkey"))
        print('✅ Dropped existing foreign key constraint')
        
        # Step 5: Rename the foreign key column in products table
        conn.execute(text("ALTER TABLE products RENAME COLUMN datatype_id TO measure_type_id"))
        print('✅ Foreign key column renamed from datatype_id to measure_type_id')
        
        # Step 6: Add new foreign key constraint
        conn.execute(text("ALTER TABLE products ADD CONSTRAINT products_measure_type_id_fkey FOREIGN KEY (measure_type_id) REFERENCES measure_type(measure_type_id)"))
        print('✅ Added new foreign key constraint')
        
        conn.commit()
        print('✅ All changes committed successfully!')
        
        # Verify the changes
        print('\n--- Verification ---')
        
        # Check if measure_type table exists
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'measure_type'
        """))
        if result.fetchone():
            print('✅ measure_type table exists')
        else:
            print('❌ measure_type table not found')
            
        # Show measure_type table structure
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'measure_type' 
            ORDER BY ordinal_position
        """))
        print('\nmeasure_type table structure:')
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
            
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
            AND kcu.column_name = 'measure_type_id'
        """))
        
        print('\nForeign key constraints:')
        for row in result:
            print(f'  {row[0]}: {row[1]}.{row[2]} -> {row[3]}.{row[4]}')
            
except Exception as e:
    print('❌ Error making changes:', e)

