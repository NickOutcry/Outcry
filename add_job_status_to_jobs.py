from database import engine
from sqlalchemy import text

print('Adding job_status_id column to job.jobs table...')
try:
    with engine.connect() as conn:
        # Add job_status_id column to job.jobs table
        conn.execute(text("ALTER TABLE job.jobs ADD COLUMN IF NOT EXISTS job_status_id INTEGER REFERENCES job.job_statuses(job_status_id)"))
        print('✅ Added job_status_id column to job.jobs')
        
        conn.commit()
        print('\n✅ Changes committed successfully!')
        
        # Verify the change
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'job' AND table_name = 'jobs'
            ORDER BY ordinal_position
        """))
        
        print('\nUpdated job.jobs table structure:')
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
            
except Exception as e:
    print('❌ Error making changes:', e)

