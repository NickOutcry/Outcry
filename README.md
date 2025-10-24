# Outcry Database Project

A comprehensive database system with four main schemas: Client, Product, Job, and Staff. Built with SQLAlchemy for robust data management and relationships.

## Database Schemas

### 1. Client Schema
Stores client information with separate contact and billing details.

**Client Table:**
- `client_id` (Primary Key, Serial)
- `name` (Text, Required)
- `address` (Text)
- `suburb` (Text)
- `state` (Text)
- `postcode` (Numeric(4))

**Contact Table:**
- `contact_id` (Primary Key, Serial)
- `first_name` (Text, Required)
- `surname` (Text, Required)
- `email` (Text)
- `phone` (Text)
- `client_id` (Foreign Key to Client)

**Billing Table:**
- `billing_id` (Primary Key, Serial)
- `entity` (Text, Required)
- `address` (Text)
- `suburb` (Text)
- `state` (Text)
- `postcode` (Numeric(4))
- `client_id` (Foreign Key to Client)

### 2. Product Schema
Manages product categories, products, variables, and options with flexible pricing.

**Product_Category Table:**
- `product_category_id` (Primary Key, Serial)
- `name` (Text, Required)

**Product Table:**
- `product_id` (Primary Key, Serial)
- `name` (Text, Required)
- `base_cost` (Numeric, Required)
- `multiplier_cost` (Numeric, Required)
- `product_category_id` (Foreign Key to Product_Category)

**Product_Variable Table:**
- `product_variable_id` (Primary Key, Serial)
- `name` (Text, Required)
- `base_cost` (Numeric, Required)
- `multiplier_cost` (Numeric, Required)
- `data_type` (Text, Required)
- `product_id` (Foreign Key to Product)

**Variable_Option Table:**
- `variable_option_id` (Primary Key, Serial)
- `name` (Text, Required)
- `base_cost` (Numeric, Required)
- `multiplier_cost` (Numeric, Required)
- `product_variable_id` (Foreign Key to Product_Variable)

### 3. Staff Schema
Tracks employee information and details.

**Fields:**
- `staff_id` (Primary Key, Serial)
- `first_name` (Text, Required)
- `surname` (Text, Required)
- `phone` (Text)
- `address` (Text)
- `suburb` (Text)
- `state` (Text - Enum_Common.State equivalent)
- `postcode` (Numeric(4))
- `dob` (Date - Date of Birth)
- `emergency_contact` (Text)
- `emergency_contact_number` (Text)

### 4. Job Schema
Manages projects, jobs, and items with detailed cost tracking.

**Project Table:**
- `project_id` (Primary Key, Serial)
- `name` (Text, Required)
- `address` (Text)
- `suburb` (Text)
- `state` (Text - Enum_Common.State equivalent)
- `postcode` (Numeric(4))
- `date_created` (Date)

**Job Table:**
- `job_id` (Primary Key, Serial)
- `reference` (Text, Required)
- `project_id` (Foreign Key to Project)
- `client_id` (Foreign Key to Client, Required)
- `po` (Text - Purchase Order)
- `date_created` (Date)
- `cost_excl_gst` (Numeric)
- `cost_incl_gst` (Numeric)
- `contact_id` (Foreign Key to Contact)
- `staff_id` (Foreign Key to Staff)

**Item Table:**
- `item_id` (Primary Key, Serial)
- `job_id` (Foreign Key to Job)
- `product_id` (Foreign Key to Product)
- `notes` (Text)
- `quantity` (Numeric, Required)
- `cost_excl_gst` (Numeric)
- `cost_incl_gst` (Numeric)

**Item_Variable Table:**
- `item_variable_id` (Primary Key, Serial)
- `item_id` (Foreign Key to Item)
- `product_variable_id` (Foreign Key to Product_Variable)

**Item_Variable_Option Table:**
- `item_variable_option_id` (Primary Key, Serial)
- `item_variable_id` (Foreign Key to Item_Variable)
- `variable_option_id` (Foreign Key to Variable_Option)

**Job_Status Table:**
- `job_status_id` (Primary Key, Serial)
- `job_status` (Text, Required)

**Job_Status_History Table:**
- `job_status_history_id` (Primary Key, Serial)
- `job_id` (Foreign Key to Job)
- `job_status_id` (Foreign Key to Job_Status)
- `date` (Date)

## Relationships

- **Client** ↔ **Contact**: One-to-Many (A client can have multiple contacts)
- **Client** ↔ **Billing**: One-to-Many (A client can have multiple billing entities)
- **Client** ↔ **Job**: One-to-Many (A client can have multiple jobs)
- **Contact** ↔ **Job**: One-to-Many (A contact can be associated with multiple jobs)
- **Product_Category** ↔ **Product**: One-to-Many (A category can have multiple products)
- **Product** ↔ **Product_Variable**: One-to-Many (A product can have multiple variables)
- **Product_Variable** ↔ **Variable_Option**: One-to-Many (A variable can have multiple options)
- **Project** ↔ **Job**: One-to-Many (A project can have multiple jobs)
- **Job** ↔ **Item**: One-to-Many (A job can have multiple items)
- **Job** ↔ **Job_Status_History**: One-to-Many (A job can have multiple status history records)
- **Job_Status** ↔ **Job_Status_History**: One-to-Many (A status can be used in multiple history records)
- **Product** ↔ **Item**: One-to-Many (A product can be used in multiple items)
- **Item** ↔ **Item_Variable**: One-to-Many (An item can have multiple variables)
- **Product_Variable** ↔ **Item_Variable**: One-to-Many (A product variable can be used in multiple item variables)
- **Item_Variable** ↔ **Item_Variable_Option**: One-to-Many (An item variable can have multiple selected options)
- **Variable_Option** ↔ **Item_Variable_Option**: One-to-Many (A variable option can be selected in multiple item variables)
- **Staff** ↔ **Job**: One-to-Many (A staff member can be assigned to multiple jobs)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Copy `env_example.txt` to `.env` and configure your database URL:
```bash
cp env_example.txt .env
```

Edit `.env` file with your database configuration:
```env
# For SQLite (default)
DATABASE_URL=sqlite:///outcry_database.db

# For PostgreSQL
# DATABASE_URL=postgresql://username:password@localhost:5432/outcry_database

# For MySQL
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/outcry_database
```

### 3. Initialize Database
```bash
python init_db.py
```

This will:
- Create all database tables
- Optionally populate with sample data

### 4. Verify Setup
The database will be created with all tables and relationships. If you chose to include sample data, you'll have:
- 3 sample clients with their contact and billing information
- 4 sample product categories
- 4 sample products with variables and options
- 3 sample staff members with complete personal information
- 3 sample projects
- 3 sample jobs with items, variables, and status history
- 5 sample job statuses
- Sample job status history records

## Usage Examples

### Basic Database Operations
```python
from database import SessionLocal
from models import Client, Contact, Billing, ProductCategory, Product, ProductVariable, VariableOption, Staff, Project, Job, Item, ItemVariable, ItemVariableOption, JobStatus, JobStatusHistory

# Get database session
db = SessionLocal()

# Create a new client
new_client = Client(
    name="New Client Company",
    address="123 Main Street",
    suburb="Downtown",
    state="NSW",
    postcode=2000
)
db.add(new_client)
db.commit()

# Create contact for the client
new_contact = Contact(
    first_name="John",
    surname="Doe",
    email="john.doe@newclient.com",
    phone="555-0123",
    client_id=new_client.client_id
)
db.add(new_contact)

# Create billing for the client
new_billing = Billing(
    entity="New Client Company Pty Ltd",
    address="123 Main Street",
    suburb="Downtown",
    state="NSW",
    postcode=2000,
    client_id=new_client.client_id
)
db.add(new_billing)

# Create a product category
new_category = ProductCategory(name="Custom Products")
db.add(new_category)
db.commit()

# Create a product
new_product = Product(
    name="Custom Widget",
    base_cost=50.00,
    multiplier_cost=2.0,
    product_category_id=new_category.product_category_id
)
db.add(new_product)
db.commit()

# Create product variables
size_variable = ProductVariable(
    name="Size",
    base_cost=0.00,
    multiplier_cost=1.0,
    data_type="select",
    product_id=new_product.product_id
)
db.add(size_variable)
db.commit()

# Create variable options
size_options = [
    VariableOption(name="Small", base_cost=0.00, multiplier_cost=1.0, product_variable_id=size_variable.product_variable_id),
    VariableOption(name="Medium", base_cost=10.00, multiplier_cost=1.1, product_variable_id=size_variable.product_variable_id),
    VariableOption(name="Large", base_cost=20.00, multiplier_cost=1.2, product_variable_id=size_variable.product_variable_id)
]
for option in size_options:
    db.add(option)
db.commit()

# Create a project
new_project = Project(
    name="New Office Setup",
    address="456 Business Ave",
    suburb="Midtown",
    state="VIC",
    postcode=3000,
    date_created=datetime.now().date()
)
db.add(new_project)
db.commit()

# Create a staff member
new_staff = Staff(
    first_name="Michael",
    surname="Johnson",
    phone="555-0204",
    address="321 Worker Lane",
    suburb="Worker District",
    state="WA",
    postcode=6000,
    dob=datetime(1988, 12, 5).date(),
    emergency_contact="Lisa Johnson",
    emergency_contact_number="555-0304"
)
db.add(new_staff)
db.commit()

# Create a job
new_job = Job(
    reference="JOB-2024-001",
    project_id=new_project.project_id,
    client_id=new_client.client_id,
    po="PO-2024-001",
    date_created=datetime.now().date(),
    cost_excl_gst=1000.00,
    cost_incl_gst=1100.00,
    contact_id=new_contact.contact_id,
    staff_id=new_staff.staff_id
)
db.add(new_job)
db.commit()

# Create job items
new_item = Item(
    job_id=new_job.job_id,
    product_id=new_product.product_id,
    notes="Custom widget for reception area",
    quantity=2,
    cost_excl_gst=100.00,
    cost_incl_gst=110.00
)
db.add(new_item)
db.commit()

# Create job statuses
pending_status = JobStatus(job_status="Pending")
in_progress_status = JobStatus(job_status="In Progress")
db.add(pending_status)
db.add(in_progress_status)
db.commit()

# Create job status history
status_history = JobStatusHistory(
    job_id=new_job.job_id,
    job_status_id=pending_status.job_status_id,
    date=datetime.now().date()
)
db.add(status_history)
db.commit()

# Create item variables
item_variable = ItemVariable(
    item_id=new_item.item_id,
    product_variable_id=size_variable.product_variable_id
)
db.add(item_variable)
db.commit()

# Create item variable options
item_variable_option = ItemVariableOption(
    item_variable_id=item_variable.item_variable_id,
    variable_option_id=size_options[1].variable_option_id  # Medium size
)
db.add(item_variable_option)
db.commit()

# Query projects with their jobs, items, and status history
projects = db.query(Project).all()
for project in projects:
    print(f"Project: {project.name}")
    for job in project.jobs:
        print(f"  Job: {job.reference} (PO: {job.po})")
        # Show status history
        for status_record in job.status_history:
            print(f"    Status: {status_record.job_status.job_status} on {status_record.date}")
        for item in job.items:
            print(f"    Item: {item.product.name} - Qty: {item.quantity}, Cost: ${item.cost_incl_gst}")
            # Show item variables and options
            for item_var in item.item_variables:
                print(f"      Variable: {item_var.product_variable.name}")
                for item_var_opt in item_var.item_variable_options:
                    print(f"        Selected: {item_var_opt.variable_option.name}")

# Close session
db.close()
```

### Querying Relationships
```python
# Get all jobs for a specific client
client_jobs = db.query(Job).filter(Job.client_id == 1).all()

# Get all products used in a specific job
job_products = db.query(JobProduct).filter(JobProduct.job_id == 1).all()

# Get staff member with their assigned jobs
staff_with_jobs = db.query(Staff).filter(Staff.id == 1).first()
assigned_jobs = staff_with_jobs.assigned_jobs
```

## Database Features

- **Automatic Timestamps**: `created_at` and `updated_at` fields are automatically managed
- **Soft Deletes**: `is_active` field allows for soft deletion of records
- **Foreign Key Constraints**: Proper relationships with referential integrity
- **Unique Constraints**: Email addresses and SKUs are unique
- **Flexible Status Management**: Jobs have status and priority fields
- **Inventory Tracking**: Products include stock quantity and minimum stock levels

## File Structure

```
├── models.py          # Database models and schemas
├── database.py        # Database configuration and connection
├── init_db.py         # Database initialization script
├── requirements.txt   # Python dependencies
├── env_example.txt    # Environment configuration example
└── README.md         # This file
```

## Supported Databases

- **SQLite** (default, file-based)
- **PostgreSQL** (recommended for production)
- **MySQL** (alternative option)

## Next Steps

Consider adding:
- API endpoints (FastAPI/Flask)
- User authentication
- Data validation
- Migration scripts (Alembic)
- Backup and recovery procedures
- Performance optimization
