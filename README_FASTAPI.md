# FastAPI Application Documentation

## Overview

This is a FastAPI-based REST API for the Outcry Projects management system. The application is organized into domain-specific schemas, models, and routers following a modular architecture.

## Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Database Schemas](#database-schemas)
- [API Routers](#api-routers)
- [Testing Endpoints](#testing-endpoints)
- [Using the API Documentation](#using-the-api-documentation)
- [Example Usage](#example-usage)

---

## Quick Start

### Prerequisites

- Python 3.7+
- PostgreSQL (or SQLite for development)
- Virtual environment (recommended)

### Installation

1. **Clone the repository** (if applicable)

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/outcry_db
# Or for SQLite:
# DATABASE_URL=sqlite:///outcry_database.db

DROPBOX_ACCESS_TOKEN=your_dropbox_token_here
GOOGLE_MAPS_API_KEY=your_google_maps_key_here

APP_NAME=Outcry Projects API
APP_VERSION=2.0.0
HOST=0.0.0.0
PORT=5001
```

5. **Run the application:**

**Option 1: Using the setup script (Recommended)**
```bash
./run.sh
```

**Option 2: Using uvicorn directly**
```bash
uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

**Option 3: Using Python**
```bash
python main.py
```

### Access the API

- **API Root**: http://localhost:5001/
- **Interactive API Docs (Swagger UI)**: http://localhost:5001/docs
- **Alternative API Docs (ReDoc)**: http://localhost:5001/redoc
- **Health Check**: http://localhost:5001/health

---

## Project Structure

```
Outcry_Projects/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and environment variables
├── database.py            # Database connection and session management
├── models/                # SQLAlchemy models organized by domain
│   ├── __init__.py
│   ├── client.py          # Client, Contact, Billing models
│   ├── product.py         # Product domain models
│   ├── job.py             # Job domain models
│   ├── staff.py           # Staff model
│   ├── delivery.py        # Delivery domain models
│   ├── throughput.py      # Throughput domain models
│   └── public.py          # Public schema models (template)
├── schemas/               # Pydantic schemas for validation
│   ├── __init__.py
│   ├── client.py
│   ├── product.py
│   ├── job.py
│   ├── staff.py
│   ├── delivery.py
│   ├── throughput.py
│   └── public.py
├── routers/               # FastAPI routers organized by domain
│   ├── __init__.py
│   ├── client.py
│   ├── product.py
│   ├── job.py
│   ├── staff.py
│   ├── delivery.py
│   ├── throughput.py
│   ├── public.py
│   └── upload.py
├── static/                # Static files
├── templates/             # Jinja2 templates
├── requirements.txt       # Python dependencies
└── run.sh                 # Setup and run script
```

---

## Database Schemas

The application uses PostgreSQL with multiple schemas to organize data by domain:

### 1. Client Schema (`client`)

**Models:**
- `Client` - Client information
- `Contact` - Client contact persons
- `Billing` - Client billing entities

**Location:** `models/client.py`

**Fields:**
- **Client**: `client_id`, `name`, `address`, `suburb`, `state`, `postcode`
- **Contact**: `contact_id`, `first_name`, `surname`, `email`, `phone`, `client_id`
- **Billing**: `billing_id`, `entity`, `address`, `suburb`, `state`, `postcode`, `client_id`

### 2. Product Schema (`product`)

**Models:**
- `ProductCategory` - Product categories
- `Product` - Products
- `ProductVariable` - Product variables/attributes
- `VariableOption` - Options for variables
- `ProductProductVariable` - Many-to-many relationship
- `MeasureType` - Measurement types

**Location:** `models/product.py`

**Fields:**
- **ProductCategory**: `product_category_id`, `name`
- **Product**: `product_id`, `name`, `product_category_id`, `measure_type_id`
- **ProductVariable**: `product_variable_id`, `name`, `data_type`
- **VariableOption**: `variable_option_id`, `name`, `base_cost`, `multiplier_cost`, `product_variable_id`

### 3. Job Schema (`job`)

**Models:**
- `Project` - Projects
- `Job` - Jobs
- `Quote` - Quotes
- `Item` - Quote items
- `ItemVariable` - Item variables
- `ItemVariableOption` - Item variable options
- `JobStatus` - Job statuses
- `JobStatusHistory` - Job status change history

**Location:** `models/job.py`

**Fields:**
- **Project**: `project_id`, `name`, `address`, `suburb`, `state`, `postcode`, `date_created`
- **Job**: `job_id`, `reference`, `project_id`, `client_id`, `contact_id`, `staff_id`, `job_status_id`, etc.
- **Quote**: `quote_id`, `quote_number`, `job_id`, `cost_excl_gst`, `cost_incl_gst`
- **Item**: `item_id`, `quote_id`, `product_id`, `quantity`, `cost_excl_gst`, `cost_incl_gst`

### 4. Staff Schema (`staff`)

**Models:**
- `Staff` - Staff/employee information

**Location:** `models/staff.py`

**Fields:**
- **Staff**: `staff_id`, `first_name`, `surname`, `phone`, `address`, `suburb`, `state`, `postcode`, `dob`, `email`, etc.

### 5. Delivery Schema (`delivery`)

**Models:**
- `Address` - Delivery addresses with geocoding
- `Booking` - Delivery bookings
- `Attachment` - File attachments

**Location:** `models/delivery.py`

**Fields:**
- **Address**: `address_id`, `name`, `google_place_id`, `formatted_address`, `latitude`, `longitude`, etc.
- **Booking**: `booking_id`, `pickup_address_id`, `pickup_date`, `dropoff_address_id`, `dropoff_date`, `completion`, etc.
- **Attachment**: `attachment_id`, `booking_id`, `dropbox_path`, `dropbox_shared_url`, `uploaded_by`, `uploaded_at`

### 6. Throughput Schema (`throughput`)

**Models:**
- `ThroughputStatus` - Task statuses
- `ThroughputStage` - Workflow stages
- `ThroughputTask` - Individual tasks
- `ThroughputStageDate` - Stage due dates

**Location:** `models/throughput.py`

**Fields:**
- **ThroughputStatus**: `status_id`, `status`
- **ThroughputStage**: `stage_id`, `stage`, `stage_order`
- **ThroughputTask**: `task_id`, `task_name`, `job_number`, `item_id`, `stage_id`, `status_id`, `task_order`, `time_completed`
- **ThroughputStageDate**: `stage_date_id`, `job_id`, `status_id`, `due_date`

### 7. Public Schema (`public`)

**Models:**
- Currently empty (template ready for future system tables)

**Location:** `models/public.py`

---

## API Routers

All routers are prefixed with `/api` and organized by domain. Each router provides full CRUD operations for its models.

### 1. Client Router (`/api`)

**Tag:** `client`

**Endpoints:**
- `GET /api/clients` - List all clients
- `GET /api/clients/{client_id}` - Get single client
- `POST /api/clients` - Create client
- `PUT /api/clients/{client_id}` - Update client
- `DELETE /api/clients/{client_id}` - Delete client
- `GET /api/contacts` - List all contacts
- `GET /api/contacts/{contact_id}` - Get single contact
- `POST /api/contacts` - Create contact
- `PUT /api/contacts/{contact_id}` - Update contact
- `DELETE /api/contacts/{contact_id}` - Delete contact
- `GET /api/billing` - List all billing entities
- `GET /api/billing/{billing_id}` - Get single billing entity
- `POST /api/billing` - Create billing entity
- `PUT /api/billing/{billing_id}` - Update billing entity
- `DELETE /api/billing/{billing_id}` - Delete billing entity
- `GET /api/clients/{client_id}/contacts` - Get client's contacts
- `GET /api/clients/{client_id}/billing-entities` - Get client's billing entities
- `GET /api/client/test` - Test endpoint (returns first records)

**Total:** 17 endpoints

### 2. Product Router (`/api`)

**Tag:** `product`

**Endpoints:**
- `GET /api/categories` - List product categories
- `GET /api/categories/{category_id}` - Get single category
- `POST /api/categories` - Create category
- `PUT /api/categories/{category_id}` - Update category
- `DELETE /api/categories/{category_id}` - Delete category
- `GET /api/measure-types` - List measure types
- `GET /api/measure-types/{measure_type_id}` - Get single measure type
- `POST /api/measure-types` - Create measure type
- `PUT /api/measure-types/{measure_type_id}` - Update measure type
- `DELETE /api/measure-types/{measure_type_id}` - Delete measure type
- `GET /api/products` - List products
- `GET /api/products/{product_id}` - Get single product
- `POST /api/products` - Create product
- `PUT /api/products/{product_id}` - Update product
- `DELETE /api/products/{product_id}` - Delete product
- `GET /api/variables` - List product variables
- `GET /api/variables/{variable_id}` - Get single variable
- `POST /api/variables` - Create variable
- `PUT /api/variables/{variable_id}` - Update variable
- `DELETE /api/variables/{variable_id}` - Delete variable
- `GET /api/variables/{variable_id}/options` - Get variable options
- `GET /api/options/{option_id}` - Get single option
- `POST /api/options` - Create option
- `PUT /api/options/{option_id}` - Update option
- `DELETE /api/options/{option_id}` - Delete option
- `GET /api/product/test` - Test endpoint

**Total:** 27 endpoints

### 3. Job Router (`/api`)

**Tag:** `job`

**Endpoints:**
- `GET /api/projects` - List projects
- `GET /api/projects/{project_id}` - Get single project
- `POST /api/projects` - Create project
- `PUT /api/projects/{project_id}` - Update project
- `DELETE /api/projects/{project_id}` - Delete project
- `GET /api/clients/{client_id}/projects` - Get client's projects
- `GET /api/job-statuses` - List job statuses
- `GET /api/job-statuses/{status_id}` - Get single status
- `POST /api/job-statuses` - Create status
- `GET /api/jobs` - List jobs
- `GET /api/jobs/{job_id}` - Get single job
- `POST /api/jobs` - Create job
- `PUT /api/jobs/{job_id}` - Update job
- `DELETE /api/jobs/{job_id}` - Delete job
- `GET /api/quotes` - List quotes
- `GET /api/quotes/{quote_id}` - Get single quote
- `POST /api/quotes` - Create quote
- `PUT /api/quotes/{quote_id}` - Update quote
- `GET /api/items` - List items
- `GET /api/items/{item_id}` - Get single item
- `POST /api/items` - Create item
- `GET /api/job/test` - Test endpoint

**Total:** 25 endpoints

### 4. Staff Router (`/api`)

**Tag:** `staff`

**Endpoints:**
- `GET /api/staff` - List all staff
- `GET /api/staff/{staff_id}` - Get single staff member
- `POST /api/staff` - Create staff member
- `PUT /api/staff/{staff_id}` - Update staff member
- `DELETE /api/staff/{staff_id}` - Delete staff member
- `GET /api/staff/test` - Test endpoint

**Total:** 6 endpoints

### 5. Delivery Router (`/api`)

**Tag:** `delivery`

**Endpoints:**
- `GET /api/addresses` - List addresses
- `GET /api/addresses/{address_id}` - Get single address
- `POST /api/addresses` - Create address
- `PUT /api/addresses/{address_id}` - Update address
- `DELETE /api/addresses/{address_id}` - Delete address
- `GET /api/bookings` - List bookings
- `GET /api/bookings/{booking_id}` - Get single booking
- `POST /api/bookings` - Create booking
- `PUT /api/bookings/{booking_id}` - Update booking
- `DELETE /api/bookings/{booking_id}` - Delete booking
- `GET /api/attachments` - List attachments (filterable by `booking_id`)
- `GET /api/attachments/{attachment_id}` - Get single attachment
- `POST /api/attachments` - Create attachment
- `PUT /api/attachments/{attachment_id}` - Update attachment
- `DELETE /api/attachments/{attachment_id}` - Delete attachment
- `GET /api/delivery/test` - Test endpoint

**Total:** 16 endpoints

### 6. Throughput Router (`/api`)

**Tag:** `throughput`

**Endpoints:**
- `GET /api/throughput/statuses` - List throughput statuses
- `GET /api/throughput/statuses/{status_id}` - Get single status
- `POST /api/throughput/statuses` - Create status
- `PUT /api/throughput/statuses/{status_id}` - Update status
- `DELETE /api/throughput/statuses/{status_id}` - Delete status
- `GET /api/throughput/stages` - List stages
- `GET /api/throughput/stages/{stage_id}` - Get single stage
- `POST /api/throughput/stages` - Create stage
- `PUT /api/throughput/stages/{stage_id}` - Update stage
- `DELETE /api/throughput/stages/{stage_id}` - Delete stage
- `GET /api/throughput/tasks` - List tasks (filterable by `job_number`, `stage_id`, `status_id`)
- `GET /api/throughput/tasks/{task_id}` - Get single task
- `POST /api/throughput/tasks` - Create task
- `PUT /api/throughput/tasks/{task_id}` - Update task
- `DELETE /api/throughput/tasks/{task_id}` - Delete task
- `GET /api/throughput/stage-dates` - List stage dates (filterable by `job_id`, `status_id`)
- `GET /api/throughput/stage-dates/{stage_date_id}` - Get single stage date
- `POST /api/throughput/stage-dates` - Create stage date
- `PUT /api/throughput/stage-dates/{stage_date_id}` - Update stage date
- `DELETE /api/throughput/stage-dates/{stage_date_id}` - Delete stage date
- `GET /api/throughput/test` - Test endpoint

**Total:** 21 endpoints

### 7. Public Router (`/api`)

**Tag:** `public`

**Endpoints:**
- `GET /api/public/test` - Test endpoint (database connection only)

**Note:** Public schema currently has no models. Add routes here when models are created.

**Total:** 1 endpoint (test only)

### 8. Upload Router (`/api`)

**Tag:** `upload`

**Endpoints:**
- `POST /api/upload` - Upload files (general)
- `POST /api/upload/job/{job_id}` - Upload files for a job
- `POST /api/upload/booking/{booking_id}` - Upload files for a booking
- `GET /api/attachments` - List attachments
- `GET /api/attachments/{attachment_id}` - Get single attachment
- `DELETE /api/attachments/{attachment_id}` - Delete attachment

**Total:** 6 endpoints

---

## Testing Endpoints

Each router includes a test endpoint that queries the first record from its tables to verify database connection and models:

- `GET /api/client/test` - Test Client, Contact, Billing tables
- `GET /api/staff/test` - Test Staff table
- `GET /api/delivery/test` - Test Address, Booking, Attachment tables
- `GET /api/throughput/test` - Test ThroughputStatus, ThroughputStage, ThroughputTask, ThroughputStageDate tables
- `GET /api/product/test` - Test ProductCategory, Product, ProductVariable tables
- `GET /api/job/test` - Test Project, Job, Quote tables
- `GET /api/public/test` - Test database connection

**Example Response:**
```json
{
  "status": "success",
  "message": "Database connection and models are working",
  "data": {
    "client": {
      "client_id": 1,
      "name": "Example Client",
      "address": "123 Main St",
      "suburb": "Sydney",
      "state": "NSW",
      "postcode": 2000
    },
    "contact": { ... },
    "billing": { ... }
  }
}
```

---

## Using the API Documentation

FastAPI automatically generates interactive API documentation:

### Swagger UI (`/docs`)

1. **Access:** http://localhost:5001/docs
2. **Features:**
   - Browse all endpoints organized by tags
   - View request/response schemas
   - Test endpoints directly in the browser
   - See example requests and responses

**How to test an endpoint:**

1. Navigate to http://localhost:5001/docs
2. Find the endpoint you want to test (organized by tags: client, product, job, etc.)
3. Click on the endpoint to expand it
4. Click "Try it out"
5. Fill in any required parameters
6. For POST/PUT requests, edit the request body JSON
7. Click "Execute"
8. View the response below

**Example: Creating a Client**

1. Go to `/docs`
2. Find `POST /api/clients` under the "client" tag
3. Click "Try it out"
4. Edit the request body:
```json
{
  "name": "Acme Corporation",
  "address": "123 Business St",
  "suburb": "Melbourne",
  "state": "VIC",
  "postcode": 3000
}
```
5. Click "Execute"
6. View the response with the created client

### ReDoc (`/redoc`)

1. **Access:** http://localhost:5001/redoc
2. **Features:**
   - Clean, readable documentation
   - Better for printing/sharing
   - All endpoints and schemas in one view

---

## Example Usage

### Using cURL

#### Client Endpoints

**Get all clients:**
```bash
curl http://localhost:5001/api/clients
```

**Create a client:**
```bash
curl -X POST http://localhost:5001/api/clients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation",
    "address": "123 Business St",
    "suburb": "Melbourne",
    "state": "VIC",
    "postcode": 3000
  }'
```

**Get a specific client:**
```bash
curl http://localhost:5001/api/clients/1
```

**Update a client:**
```bash
curl -X PUT http://localhost:5001/api/clients/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation Updated",
    "address": "456 New St",
    "suburb": "Sydney",
    "state": "NSW",
    "postcode": 2000
  }'
```

**Delete a client:**
```bash
curl -X DELETE http://localhost:5001/api/clients/1
```

#### Product Endpoints

**Get all products:**
```bash
curl http://localhost:5001/api/products
```

**Create a product:**
```bash
curl -X POST http://localhost:5001/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Signage",
    "product_category_id": 1,
    "measure_type_id": 1
  }'
```

**Get products with pagination:**
```bash
curl "http://localhost:5001/api/products?skip=0&limit=10"
```

#### Job Endpoints

**Get all jobs:**
```bash
curl http://localhost:5001/api/jobs
```

**Create a job:**
```bash
curl -X POST http://localhost:5001/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "reference": "JOB-2024-001",
    "project_id": 1,
    "client_id": 1,
    "contact_id": 1,
    "staff_id": 1
  }'
```

**Get client's projects:**
```bash
curl http://localhost:5001/api/clients/1/projects
```

#### Delivery Endpoints

**Get all addresses:**
```bash
curl http://localhost:5001/api/addresses
```

**Create a booking:**
```bash
curl -X POST http://localhost:5001/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_date": "2024-01-15",
    "dropoff_date": "2024-01-16",
    "pickup_time": "09:00:00",
    "dropoff_time": "17:00:00",
    "creator_id": 1,
    "completion": false
  }'
```

**Get attachments for a booking:**
```bash
curl "http://localhost:5001/api/attachments?booking_id=1"
```

#### Throughput Endpoints

**Get all throughput tasks:**
```bash
curl http://localhost:5001/api/throughput/tasks
```

**Get tasks for a specific job:**
```bash
curl "http://localhost:5001/api/throughput/tasks?job_number=1"
```

**Create a throughput status:**
```bash
curl -X POST http://localhost:5001/api/throughput/statuses \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress"
  }'
```

#### Upload Endpoints

**Upload files:**
```bash
curl -X POST http://localhost:5001/api/upload \
  -F "files=@document1.pdf" \
  -F "files=@image1.jpg" \
  -F "entity_id=1" \
  -F "entity_type=booking" \
  -F "uploaded_by=1"
```

**Upload files for a specific job:**
```bash
curl -X POST http://localhost:5001/api/upload/job/1 \
  -F "files=@document.pdf" \
  -F "uploaded_by=1"
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:5001/api"

# Get all clients
response = requests.get(f"{BASE_URL}/clients")
clients = response.json()

# Create a client
new_client = {
    "name": "Acme Corporation",
    "address": "123 Business St",
    "suburb": "Melbourne",
    "state": "VIC",
    "postcode": 3000
}
response = requests.post(f"{BASE_URL}/clients", json=new_client)
created_client = response.json()

# Update a client
update_data = {
    "name": "Acme Corporation Updated",
    "address": "456 New St"
}
response = requests.put(f"{BASE_URL}/clients/1", json=update_data)

# Delete a client
response = requests.delete(f"{BASE_URL}/clients/1")
```

### Using JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://localhost:5001/api';

// Get all clients
fetch(`${BASE_URL}/clients`)
  .then(response => response.json())
  .then(data => console.log(data));

// Create a client
fetch(`${BASE_URL}/clients`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'Acme Corporation',
    address: '123 Business St',
    suburb: 'Melbourne',
    state: 'VIC',
    postcode: 3000
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## Response Formats

### Success Response

Most endpoints return data directly:

```json
{
  "client_id": 1,
  "name": "Acme Corporation",
  "address": "123 Business St",
  "suburb": "Melbourne",
  "state": "VIC",
  "postcode": 3000
}
```

### List Response

List endpoints return arrays:

```json
[
  {
    "client_id": 1,
    "name": "Client 1",
    ...
  },
  {
    "client_id": 2,
    "name": "Client 2",
    ...
  }
]
```

### Error Response

Error responses follow this format:

```json
{
  "detail": "Client not found"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `204` - No Content (successful delete)
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

---

## Key Features

1. **Automatic API Documentation** - Swagger UI and ReDoc
2. **Request Validation** - Pydantic schemas validate all inputs
3. **Type Safety** - Full type hints throughout
4. **Dependency Injection** - Database sessions managed automatically
5. **CORS Support** - Configurable CORS middleware
6. **File Uploads** - Dropbox integration for file storage
7. **Modular Architecture** - Organized by domain schemas
8. **Test Endpoints** - Built-in endpoints to verify database connections

---

## Troubleshooting

### Database Connection Issues

1. **Check DATABASE_URL in `.env`:**
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/outcry_db
   ```

2. **Verify database is running:**
   ```bash
   psql -h localhost -U postgres -d outcry_db
   ```

3. **Test connection using test endpoints:**
   ```bash
   curl http://localhost:5001/api/client/test
   ```

### Import Errors

If you see import errors:
1. Ensure virtual environment is activated
2. Install dependencies: `pip install -r requirements.txt`
3. Check that all model files are in `models/` directory
4. Verify `schemas/` directory exists with all schema files

### Port Already in Use

If port 5001 is in use:
1. Change `PORT` in `.env` file
2. Or specify port when running:
   ```bash
   uvicorn main:app --port 5002
   ```

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Pydantic Documentation**: https://docs.pydantic.dev/

---

## Summary

- **Total Endpoints**: 124+ across 8 routers
- **Schemas**: 7 database schemas (client, product, job, staff, delivery, throughput, public)
- **Models**: 25+ SQLAlchemy models
- **Pydantic Schemas**: 75+ schemas for validation
- **Test Endpoints**: 7 test endpoints for database verification

The API is fully functional and ready for frontend integration. Use `/docs` for interactive testing and exploration of all available endpoints.
