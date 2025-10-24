from database import engine
from sqlalchemy import text

print('Adding reference column to job.items table...')
try:
    with engine.connect() as conn:
        # Add reference column to job.items table
        conn.execute(text("ALTER TABLE job.items ADD COLUMN IF NOT EXISTS reference TEXT NOT NULL DEFAULT ''"))
        print('✅ Added reference column to job.items')
        
        conn.commit()
        print('\n✅ Changes committed successfully!')
        
        # Verify the change
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_schema = 'job' AND table_name = 'items'
            ORDER BY ordinal_position
        """))
        
        print('\nUpdated job.items table structure:')
        for row in result:
            print(f'  {row[0]} ({row[1]}) - nullable: {row[2]} - default: {row[3]}')
            
except Exception as e:
    print('❌ Error making changes:', e)

