from database import engine
from sqlalchemy import text

print('Updating job and item tables...')
try:
    with engine.connect() as conn:
        # Step 1: Remove cost columns from job.job table
        print('Removing cost columns from job.job table...')
        
        # Drop the columns
        conn.execute(text("ALTER TABLE job.jobs DROP COLUMN IF EXISTS cost_excl_gst"))
        print('✅ Removed cost_excl_gst column from job.jobs')
        
        conn.execute(text("ALTER TABLE job.jobs DROP COLUMN IF EXISTS cost_incl_gst"))
        print('✅ Removed cost_incl_gst column from job.jobs')
        
        # Step 2: Update job.item table to reference quotes instead of jobs
        print('\nUpdating job.item table to reference quotes...')
        
        # Drop the existing foreign key constraint
        conn.execute(text("ALTER TABLE job.items DROP CONSTRAINT IF EXISTS items_job_id_fkey"))
        print('✅ Dropped existing foreign key constraint')
        
        # Rename the column from job_id to quote_id
        conn.execute(text("ALTER TABLE job.items RENAME COLUMN job_id TO quote_id"))
        print('✅ Renamed job_id to quote_id in job.items')
        
        # Add new foreign key constraint to quote table
        conn.execute(text("ALTER TABLE job.items ADD CONSTRAINT items_quote_id_fkey FOREIGN KEY (quote_id) REFERENCES job.quote(quote_id)"))
        print('✅ Added new foreign key constraint to job.quote')
        
        conn.commit()
        print('\n✅ All changes committed successfully!')
        
        # Step 3: Verify the changes
        print('\n--- Verification ---')
        
        # Check job.jobs table structure
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'job' AND table_name = 'jobs'
            ORDER BY ordinal_position
        """))
        
        print('\njob.jobs table structure:')
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
        
        # Check job.items table structure
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'job' AND table_name = 'items'
            ORDER BY ordinal_position
        """))
        
        print('\njob.items table structure:')
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
        
        # Check foreign key constraints for items table
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
            AND tc.table_schema = 'job' 
            AND tc.table_name = 'items'
        """))
        
        print('\njob.items foreign key constraints:')
        for row in result:
            print(f'  {row[0]}: {row[1]}.{row[2]} -> {row[3]}.{row[4]}')
            
except Exception as e:
    print('❌ Error making changes:', e)

