from database import engine
from sqlalchemy import text

print('Testing PostgreSQL connection...')
try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('Connection successful!')
        print('Database URL:', engine.url)
except Exception as e:
    print('Connection failed:', e)

