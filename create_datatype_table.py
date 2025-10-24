from database import engine
from sqlalchemy import text

print('Creating datatype table in PostgreSQL database...')
try:
    with engine.connect() as conn:
        # Create the datatype table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS datatype (
                datatype_id SERIAL PRIMARY KEY,
                datatype TEXT NOT NULL
            )
        """))
        conn.commit()
        print('✅ Datatype table created successfully!')
        
        # Verify the table was created
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'datatype'
        """))
        if result.fetchone():
            print('✅ Table verification successful!')
            
            # Show table structure
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'datatype' 
                ORDER BY ordinal_position
            """))
            print('\nDatatype table structure:')
            for row in result:
                print(f'  {row[0]} ({row[1]}) - nullable: {row[2]}')
        else:
            print('❌ Table creation failed!')
            
except Exception as e:
    print('❌ Error creating table:', e)

