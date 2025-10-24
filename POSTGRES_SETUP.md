# PostgreSQL Database Setup Guide

This guide will help you create the `outcry_db` database in pgAdmin4 and configure the application to use it.

## Prerequisites

- PostgreSQL server running on localhost:5432
- pgAdmin4 installed and accessible
- User `postgres` with password `gdn55L!VSpo`

## Method 1: Using pgAdmin4 (Manual)

### Step 1: Open pgAdmin4
1. Launch pgAdmin4
2. Connect to your PostgreSQL server using:
   - Host: localhost
   - Port: 5432
   - Username: postgres
   - Password: gdn55L!VSpo

### Step 2: Create Database
1. Right-click on "Databases" in the left panel
2. Select "Create" → "Database..."
3. In the "Create Database" dialog:
   - **Database**: `outcry_db`
   - **Owner**: `postgres`
   - Click "Save"

### Step 3: Verify Database Creation
1. Expand "Databases" in the left panel
2. You should see `outcry_db` listed
3. Expand `outcry_db` to see it's empty (no tables yet)

## Method 2: Using the Setup Script (Recommended)

### Step 1: Run the Setup Script
```bash
python setup_postgres.py
```

This script will:
- Create the `outcry_db` database if it doesn't exist
- Create all the required tables
- Optionally populate with sample data

### Step 2: Verify Setup
1. Open pgAdmin4
2. Connect to your PostgreSQL server
3. Navigate to `outcry_db` → `Schemas` → `public` → `Tables`
4. You should see all the tables created:
   - clients
   - contacts
   - billing
   - product_categories
   - products
   - product_variables
   - variable_options
   - staff
   - projects
   - jobs
   - items
   - item_variables
   - item_variable_options
   - job_statuses
   - job_status_history

## Method 3: Using SQL Commands

### Step 1: Connect to PostgreSQL
```bash
psql -h localhost -p 5432 -U postgres -d postgres
```

### Step 2: Create Database
```sql
CREATE DATABASE outcry_db;
```

### Step 3: Exit psql
```sql
\q
```

### Step 4: Run Python Setup
```bash
python setup_postgres.py
```

## Configuration

The application is configured to use PostgreSQL with these settings:

- **Host**: localhost
- **Port**: 5432
- **Database**: outcry_db
- **Username**: postgres
- **Password**: gdn55L!VSpo

The connection string is: `postgresql://postgres:gdn55L!VSpo@localhost:5432/outcry_db`

## Troubleshooting

### Connection Issues
1. **PostgreSQL not running**: Start PostgreSQL service
2. **Wrong password**: Verify the password is `gdn55L!VSpo`
3. **Port issues**: Ensure PostgreSQL is running on port 5432
4. **Permission denied**: Make sure user `postgres` has permission to create databases

### Database Creation Issues
1. **Database already exists**: The script will handle this automatically
2. **Permission denied**: Run as a user with database creation privileges
3. **Connection timeout**: Check if PostgreSQL is accessible on localhost:5432

### Table Creation Issues
1. **Import errors**: Make sure all Python dependencies are installed
2. **Schema conflicts**: Drop and recreate the database if needed
3. **Foreign key errors**: Tables are created in the correct order automatically

## Verification

After setup, you can verify everything is working by:

1. **Checking tables in pgAdmin4**:
   - Navigate to `outcry_db` → `Schemas` → `public` → `Tables`
   - You should see all 15 tables listed

2. **Running a test query**:
   ```python
   from database import SessionLocal
   from models import Client
   
   db = SessionLocal()
   clients = db.query(Client).all()
   print(f"Found {len(clients)} clients")
   db.close()
   ```

3. **Checking sample data** (if created):
   - In pgAdmin4, right-click on any table and select "View/Edit Data" → "All Rows"
   - You should see sample data if you chose to create it

## Next Steps

Once the database is set up, you can:

1. **Start using the application** with the new PostgreSQL database
2. **Add your own data** through the application
3. **Create additional indexes** for performance optimization
4. **Set up backups** for the PostgreSQL database
5. **Configure connection pooling** for production use

## Security Notes

- The password is stored in plain text in the configuration
- For production, consider using environment variables or a secure configuration management system
- Ensure the PostgreSQL server is properly secured with firewall rules
- Consider using SSL connections for production deployments

