from database import engine
from sqlalchemy import text

print('Creating schemas and reorganizing tables...')
try:
    with engine.connect() as conn:
        # Step 1: Create the schemas
        schemas = ['client', 'product', 'job', 'staff']
        for schema in schemas:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            print(f'✅ Created schema: {schema}')
        
        # Step 2: Create the new quote table in job schema
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS job.quote (
                quote_id SERIAL PRIMARY KEY,
                date_created DATE DEFAULT CURRENT_DATE,
                cost_excl_gst DOUBLE PRECISION,
                cost_incl_gst DOUBLE PRECISION
            )
        """))
        print('✅ Created quote table in job schema')
        
        # Step 3: Move tables to their respective schemas
        table_moves = [
            # Client schema
            ('clients', 'client.clients'),
            ('contacts', 'client.contacts'),
            ('billing', 'client.billing'),
            
            # Product schema
            ('product_categories', 'product.product_categories'),
            ('products', 'product.products'),
            ('product_variables', 'product.product_variables'),
            ('variable_options', 'product.variable_options'),
            ('measure_type', 'product.measure_type'),
            
            # Job schema
            ('projects', 'job.projects'),
            ('jobs', 'job.jobs'),
            ('items', 'job.items'),
            ('item_variables', 'job.item_variables'),
            ('item_variable_options', 'job.item_variable_options'),
            ('job_statuses', 'job.job_statuses'),
            ('job_status_history', 'job.job_status_history'),
            
            # Staff schema
            ('staff', 'staff.staff')
        ]
        
        for old_table, new_table in table_moves:
            try:
                # Check if table exists in public schema
                result = conn.execute(text(f"""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = '{old_table}'
                """))
                
                if result.fetchone():
                    # Move table to new schema
                    conn.execute(text(f"ALTER TABLE {old_table} SET SCHEMA {new_table.split('.')[0]}"))
                    print(f'✅ Moved {old_table} to {new_table}')
                else:
                    print(f'⚠️  Table {old_table} not found in public schema')
            except Exception as e:
                print(f'⚠️  Could not move {old_table}: {e}')
        
        conn.commit()
        print('✅ All changes committed successfully!')
        
        # Step 4: Verify the new structure
        print('\n--- Verification ---')
        
        for schema in schemas:
            result = conn.execute(text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = '{schema}'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            print(f'\n{schema.upper()} Schema Tables:')
            for table in tables:
                print(f'  - {table}')
        
        # Step 5: Show quote table structure
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'job' AND table_name = 'quote'
            ORDER BY ordinal_position
        """))
        
        print('\nQuote table structure:')
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
            
except Exception as e:
    print('❌ Error creating schemas:', e)

