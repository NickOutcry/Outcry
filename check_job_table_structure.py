from database import engine
from sqlalchemy import text

print('Checking job.jobs table structure...')
try:
    with engine.connect() as conn:
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
            
except Exception as e:
    print('❌ Error checking table structure:', e)

