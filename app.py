from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import SessionLocal
from models import (
    Product, ProductCategory, ProductVariable, ProductProductVariable, VariableOption,
    Quote, Client, Contact, Billing, Job, Project, JobStatus, JobStatusHistory,
    Staff, Item, ItemVariable, ItemVariableOption, MeasureType, Address, Booking, Attachment
)
import os
import json
from datetime import datetime, date, time
from typing import List, Optional
from schemas import (
    CategoryCreate, CategoryResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    VariableCreate, VariableUpdate, VariableResponse,
    OptionCreate, OptionUpdate, OptionResponse,
    ClientCreate, ClientUpdate, ClientResponse,
    ContactCreate, ContactUpdate, ContactResponse,
    BillingCreate, BillingUpdate, BillingResponse,
    StaffCreate, StaffUpdate, StaffResponse,
    ProjectCreate, ProjectUpdate, ProjectResponse,
    JobCreate, JobUpdate, JobResponse,
    ItemCreate, ItemResponse,
    ItemVariableCreate, ItemVariableResponse,
    QuoteCreate, QuoteUpdate, QuoteDetailResponse,
    JobStatusUpdate, JobAddressUpdate, JobBillingUpdate, ApproveQuoteRequest,
    StageResponse, StageUpdate, StageDueDateUpdate,
    TaskCreate, TaskResponse, TaskStatusUpdate,
    BookingCreate, BookingUpdate, BookingResponse,
    VariableOptionCostsRequest, VariableOptionCostResponse
)

# Import routers
from routers import client_router, product_router, job_router, staff_router, upload_router

# Import configuration
from config import (
    DROPBOX_AVAILABLE,
    DROPBOX_ACCESS_TOKEN,
    GOOGLE_MAPS_API_KEY,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS,
    APP_NAME,
    APP_VERSION
)

# Try to import dropbox_service, but make it optional
try:
    from dropbox_service import initialize_dropbox_service, get_dropbox_service
except ImportError:
    print("Warning: dropbox_service not available")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize Dropbox service (if available)
if DROPBOX_AVAILABLE and DROPBOX_ACCESS_TOKEN:
    try:
        initialize_dropbox_service(DROPBOX_ACCESS_TOKEN)
        print("Dropbox service initialized successfully")
    except Exception as e:
        print(f"Warning: Failed to initialize Dropbox service: {str(e)}")
elif DROPBOX_AVAILABLE:
    print("Warning: DROPBOX_ACCESS_TOKEN not found in environment variables")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include routers
app.include_router(client_router)
app.include_router(product_router)
app.include_router(job_router)
app.include_router(staff_router)
app.include_router(upload_router)

# Routes for serving HTML pages
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/google-maps-key")
async def get_google_maps_key():
    """Return Google Maps API key for client-side use"""
    from config import GOOGLE_MAPS_API_KEY
    return {"apiKey": GOOGLE_MAPS_API_KEY}

# API Routes for Product Categories
@app.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(ProductCategory).all()
    return [{
        "product_category_id": cat.product_category_id,
        "name": cat.name
    } for cat in categories]

@app.post("/api/categories")
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        new_category = ProductCategory(name=category.name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return {
            "product_category_id": new_category.product_category_id,
            "name": new_category.name
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/categories/{category_id}")
async def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    try:
        category_obj = db.query(ProductCategory).filter(ProductCategory.product_category_id == category_id).first()
        if not category_obj:
            raise HTTPException(status_code=404, detail="Category not found")
        
        category_obj.name = category.name
        db.commit()
        
        return {
            "product_category_id": category_obj.product_category_id,
            "name": category_obj.name
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/categories/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(ProductCategory).filter(ProductCategory.product_category_id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Check if category has products
        if category.products:
            raise HTTPException(status_code=400, detail="Cannot delete category with existing products")
        
        db.delete(category)
        db.commit()
        return {"message": "Category deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Measure Types
@app.get("/api/measure-types")
async def get_measure_types(db: Session = Depends(get_db)):
    measure_types = db.query(MeasureType).all()
    return [{
        "measure_type_id": mt.measure_type_id,
        "measure_type": mt.measure_type
    } for mt in measure_types]

# API Routes for Products
@app.get("/api/products")
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    result = []
    for product in products:
        product_data = {
            "product_id": product.product_id,
            "name": product.name,
            "base_cost": 0.0,
            "multiplier_cost": 0.0,
            "product_category_id": product.product_category_id,
            "category_name": product.category.name if product.category else None,
            "measure_type_id": product.measure_type_id,
            "measure_type_name": product.measure_type.measure_type if product.measure_type else None,
            "variables": []
        }
        
        for variable in product.variables:
            variable_data = {
                "product_variable_id": variable.product_variable_id,
                "name": variable.name,
                "base_cost": 0.0,
                "multiplier_cost": 0.0,
                "data_type": variable.data_type,
                "options": []
            }
            
            for option in variable.options:
                option_data = {
                    "variable_option_id": option.variable_option_id,
                    "name": option.name,
                    "base_cost": float(option.base_cost),
                    "multiplier_cost": float(option.multiplier_cost)
                }
                variable_data["options"].append(option_data)
            
            product_data["variables"].append(variable_data)
        
        result.append(product_data)
    
    return result

@app.post("/api/products", response_model=dict)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        new_product = Product(
            name=product.name,
            product_category_id=product.product_category_id,
            measure_type_id=product.measure_type_id
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        return {
            "product_id": new_product.product_id,
            "name": new_product.name,
            "base_cost": 0.0,
            "multiplier_cost": 0.0,
            "product_category_id": new_product.product_category_id,
            "measure_type_id": new_product.measure_type_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/products/{product_id}")
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    try:
        product_obj = db.query(Product).filter(Product.product_id == product_id).first()
        if not product_obj:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product_obj.name = product.name
        product_obj.product_category_id = product.product_category_id
        product_obj.measure_type_id = product.measure_type_id
        
        db.commit()
        
        return {
            "product_id": product_obj.product_id,
            "name": product_obj.name,
            "base_cost": 0.0,
            "multiplier_cost": 0.0,
            "product_category_id": product_obj.product_category_id,
            "measure_type_id": product_obj.measure_type_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Product Variables
@app.get("/api/variables")
async def list_variables(db: Session = Depends(get_db)):
    variables = db.query(ProductVariable).all()
    result = []
    for variable in variables:
        variable_data = {
            "product_variable_id": variable.product_variable_id,
            "name": variable.name,
            "base_cost": 0.0,
            "multiplier_cost": 0.0,
            "data_type": variable.data_type,
            "product_ids": [assignment.product_id for assignment in variable.product_assignments],
            "options": []
        }
        for option in variable.options:
            option_data = {
                "variable_option_id": option.variable_option_id,
                "name": option.name,
                "base_cost": float(option.base_cost),
                "multiplier_cost": float(option.multiplier_cost)
            }
            variable_data["options"].append(option_data)
        result.append(variable_data)
    return result

@app.post("/api/variables")
async def create_variable(variable: VariableCreate, db: Session = Depends(get_db)):
    try:
        new_variable = ProductVariable(
            name=variable.name,
            data_type=variable.data_type
        )
        db.add(new_variable)
        db.flush()
        
        assigned_products = []
        if variable.product_id:
            max_order = (
                db.query(func.coalesce(func.max(ProductProductVariable.display_order), 0))
                .filter(ProductProductVariable.product_id == variable.product_id)
                .scalar()
            ) or 0
            order_value = variable.display_order if variable.display_order is not None else (max_order + 1)
            assignment = ProductProductVariable(
                product_id=variable.product_id,
                product_variable_id=new_variable.product_variable_id,
                display_order=order_value
            )
            db.add(assignment)
            assigned_products.append(variable.product_id)
        
        db.commit()
        db.refresh(new_variable)
        
        return {
            "product_variable_id": new_variable.product_variable_id,
            "name": new_variable.name,
            "base_cost": 0.0,
            "multiplier_cost": 0.0,
            "data_type": new_variable.data_type,
            "product_ids": assigned_products
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/variables/{variable_id}")
async def delete_variable(variable_id: int, db: Session = Depends(get_db)):
    try:
        variable = db.query(ProductVariable).filter(ProductVariable.product_variable_id == variable_id).first()
        if not variable:
            raise HTTPException(status_code=404, detail="Variable not found")
        
        db.query(VariableOption).filter(VariableOption.product_variable_id == variable_id).delete()
        db.delete(variable)
        db.commit()
        return {"message": "Variable deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/variables/{variable_id}")
async def update_variable(variable_id: int, variable: VariableUpdate, db: Session = Depends(get_db)):
    try:
        variable_obj = db.query(ProductVariable).filter(ProductVariable.product_variable_id == variable_id).first()
        if not variable_obj:
            raise HTTPException(status_code=404, detail="Variable not found")
        
        variable_obj.name = variable.name
        variable_obj.data_type = variable.data_type
        db.commit()
        
        return {
            "product_variable_id": variable_obj.product_variable_id,
            "name": variable_obj.name,
            "base_cost": 0.0,
            "multiplier_cost": 0.0,
            "data_type": variable_obj.data_type,
            "product_ids": [assignment.product_id for assignment in variable_obj.product_assignments]
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Variable Options
@app.post("/api/options")
async def create_option(option: OptionCreate, db: Session = Depends(get_db)):
    try:
        new_option = VariableOption(
            name=option.name,
            base_cost=option.base_cost,
            multiplier_cost=option.multiplier_cost,
            product_variable_id=option.product_variable_id
        )
        db.add(new_option)
        db.commit()
        db.refresh(new_option)
        
        return {
            "variable_option_id": new_option.variable_option_id,
            "name": new_option.name,
            "base_cost": float(new_option.base_cost),
            "multiplier_cost": float(new_option.multiplier_cost),
            "product_variable_id": new_option.product_variable_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/options/{option_id}")
async def update_option(option_id: int, option: OptionUpdate, db: Session = Depends(get_db)):
    try:
        option_obj = db.query(VariableOption).filter(VariableOption.variable_option_id == option_id).first()
        if not option_obj:
            raise HTTPException(status_code=404, detail="Option not found")
        
        option_obj.name = option.name
        option_obj.base_cost = option.base_cost
        option_obj.multiplier_cost = option.multiplier_cost
        db.commit()
        
        return {
            "variable_option_id": option_obj.variable_option_id,
            "name": option_obj.name,
            "base_cost": float(option_obj.base_cost),
            "multiplier_cost": float(option_obj.multiplier_cost),
            "product_variable_id": option_obj.product_variable_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/options/{option_id}")
async def delete_option(option_id: int, db: Session = Depends(get_db)):
    try:
        option = db.query(VariableOption).filter(VariableOption.variable_option_id == option_id).first()
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")
        
        db.delete(option)
        db.commit()
        return {"message": "Option deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Clients
@app.get("/api/clients")
async def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    result = []
    for client in clients:
        client_data = {
            "client_id": client.client_id,
            "name": client.name,
            "address": client.address,
            "suburb": client.suburb,
            "state": client.state,
            "postcode": client.postcode,
            "contacts": [],
            "billing": []
        }
        for contact in client.contacts:
            client_data["contacts"].append({
                "contact_id": contact.contact_id,
                "first_name": contact.first_name,
                "surname": contact.surname,
                "email": contact.email,
                "phone": contact.phone,
                "client_id": contact.client_id
            })
        for bill in client.billing:
            client_data["billing"].append({
                "billing_id": bill.billing_id,
                "entity": bill.entity,
                "address": bill.address,
                "suburb": bill.suburb,
                "state": bill.state,
                "postcode": bill.postcode
            })
        result.append(client_data)
    return result

@app.post("/api/clients")
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        new_client = Client(
            name=client.name,
            address=client.address,
            suburb=client.suburb,
            state=client.state,
            postcode=client.postcode
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return {
            "client_id": new_client.client_id,
            "name": new_client.name,
            "address": new_client.address,
            "suburb": new_client.suburb,
            "state": new_client.state,
            "postcode": new_client.postcode
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/clients/{client_id}")
async def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    try:
        client_obj = db.query(Client).filter(Client.client_id == client_id).first()
        if not client_obj:
            raise HTTPException(status_code=404, detail="Client not found")
        
        if client.name is not None:
            client_obj.name = client.name
        if client.address is not None:
            client_obj.address = client.address
        if client.suburb is not None:
            client_obj.suburb = client.suburb
        if client.state is not None:
            client_obj.state = client.state
        if client.postcode is not None:
            client_obj.postcode = client.postcode
        
        db.commit()
        return {
            "client_id": client_obj.client_id,
            "name": client_obj.name,
            "address": client_obj.address,
            "suburb": client_obj.suburb,
            "state": client_obj.state,
            "postcode": client_obj.postcode
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/clients/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    try:
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        db.delete(client)
        db.commit()
        return {"message": "Client deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Contacts
@app.post("/api/contacts")
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        new_contact = Contact(
            first_name=contact.first_name,
            surname=contact.surname,
            email=contact.email,
            phone=contact.phone,
            client_id=contact.client_id
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return {
            "contact_id": new_contact.contact_id,
            "first_name": new_contact.first_name,
            "surname": new_contact.surname,
            "email": new_contact.email,
            "phone": new_contact.phone,
            "client_id": new_contact.client_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    try:
        contact_obj = db.query(Contact).filter(Contact.contact_id == contact_id).first()
        if not contact_obj:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        if contact.first_name is not None:
            contact_obj.first_name = contact.first_name
        if contact.surname is not None:
            contact_obj.surname = contact.surname
        if contact.email is not None:
            contact_obj.email = contact.email
        if contact.phone is not None:
            contact_obj.phone = contact.phone
        
        db.commit()
        return {
            "contact_id": contact_obj.contact_id,
            "first_name": contact_obj.first_name,
            "surname": contact_obj.surname,
            "email": contact_obj.email,
            "phone": contact_obj.phone,
            "client_id": contact_obj.client_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    try:
        contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        db.delete(contact)
        db.commit()
        return {"message": "Contact deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Billing
@app.post("/api/billing")
async def create_billing(billing: BillingCreate, db: Session = Depends(get_db)):
    try:
        new_billing = Billing(
            entity=billing.entity,
            address=billing.address,
            suburb=billing.suburb,
            state=billing.state,
            postcode=billing.postcode,
            client_id=billing.client_id
        )
        db.add(new_billing)
        db.commit()
        db.refresh(new_billing)
        return {
            "billing_id": new_billing.billing_id,
            "entity": new_billing.entity,
            "address": new_billing.address,
            "suburb": new_billing.suburb,
            "state": new_billing.state,
            "postcode": new_billing.postcode,
            "client_id": new_billing.client_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/billing/{billing_id}")
async def update_billing(billing_id: int, billing: BillingUpdate, db: Session = Depends(get_db)):
    try:
        billing_obj = db.query(Billing).filter(Billing.billing_id == billing_id).first()
        if not billing_obj:
            raise HTTPException(status_code=404, detail="Billing not found")
        
        if billing.entity is not None:
            billing_obj.entity = billing.entity
        if billing.address is not None:
            billing_obj.address = billing.address
        if billing.suburb is not None:
            billing_obj.suburb = billing.suburb
        if billing.state is not None:
            billing_obj.state = billing.state
        if billing.postcode is not None:
            billing_obj.postcode = billing.postcode
        
        db.commit()
        return {
            "billing_id": billing_obj.billing_id,
            "entity": billing_obj.entity,
            "address": billing_obj.address,
            "suburb": billing_obj.suburb,
            "state": billing_obj.state,
            "postcode": billing_obj.postcode,
            "client_id": billing_obj.client_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/billing/{billing_id}")
async def delete_billing(billing_id: int, db: Session = Depends(get_db)):
    try:
        billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
        if not billing:
            raise HTTPException(status_code=404, detail="Billing not found")
        
        db.delete(billing)
        db.commit()
        return {"message": "Billing deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/clients/{client_id}/billing-entities")
async def get_client_billing_entities(client_id: int, db: Session = Depends(get_db)):
    billing_entities = db.query(Billing).filter(Billing.client_id == client_id).all()
    return [{
        "billing_id": billing.billing_id,
        "entity": billing.entity,
        "address": billing.address,
        "suburb": billing.suburb,
        "state": billing.state,
        "postcode": billing.postcode
    } for billing in billing_entities]

# Helper function for generating quote numbers
def generate_quote_number(job_id: int, db: Session) -> str:
    existing_quotes = db.query(Quote).filter(Quote.job_id == job_id).count()
    next_quote_number = existing_quotes + 1
    return f"{job_id}-{next_quote_number:03d}"

# API Routes for Jobs
@app.get("/api/jobs")
async def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    result = []
    for job in jobs:
        client = db.query(Client).filter(Client.client_id == job.client_id).first()
        project = db.query(Project).filter(Project.project_id == job.project_id).first()
        contact = db.query(Contact).filter(Contact.contact_id == job.contact_id).first()
        staff = db.query(Staff).filter(Staff.staff_id == job.staff_id).first()
        job_status = db.query(JobStatus).filter(JobStatus.job_status_id == job.job_status_id).first()
        
        billing = None
        if job.billing_entity:
            billing = db.query(Billing).filter(Billing.billing_id == job.billing_entity).first()
        
        client_billing_entities = db.query(Billing).filter(Billing.client_id == job.client_id).all()
        
        stage_due_date = None
        if job.stage_id:
            from models import ThroughputStageDate
            stage_date = db.query(ThroughputStageDate).filter(
                ThroughputStageDate.job_id == job.job_id,
                ThroughputStageDate.status_id == job.stage_id
            ).first()
            stage_due_date = stage_date.due_date if stage_date and stage_date.due_date else None
        
        job_data = {
            "job_id": job.job_id,
            "reference": job.reference,
            "client_id": job.client_id,
            "project_id": job.project_id,
            "contact_id": job.contact_id,
            "staff_id": job.staff_id,
            "billing_entity": job.billing_entity,
            "po": job.po,
            "date_created": job.date_created,
            "job_status_id": job.job_status_id,
            "job_address": job.job_address,
            "suburb": job.suburb,
            "state": job.state,
            "postcode": job.postcode,
            "approved_quote": job.approved_quote,
            "stage_id": job.stage_id,
            "stage_due_date": stage_due_date.isoformat() if stage_due_date else None,
            "client_name": client.name if client else None,
            "project_name": project.name if project else None,
            "contact_name": f"{contact.first_name} {contact.surname}" if contact else None,
            "staff_name": f"{staff.first_name} {staff.surname}" if staff else None,
            "staff_first_name": staff.first_name if staff else None,
            "staff_surname": staff.surname if staff else None,
            "staff_email": staff.email if staff else None,
            "staff_phone": staff.phone if staff else None,
            "billing_entity_name": billing.entity if billing else None,
            "billing_address": billing.address if billing else None,
            "billing_suburb": billing.suburb if billing else None,
            "billing_state": billing.state if billing else None,
            "billing_postcode": billing.postcode if billing else None,
            "billing_entities": [{
                "billing_id": b.billing_id,
                "entity": b.entity,
                "address": b.address,
                "suburb": b.suburb,
                "state": b.state,
                "postcode": b.postcode
            } for b in client_billing_entities],
            "job_status": job_status.job_status if job_status else None,
            "status_history": [],
            "quotes": []
        }
        
        status_history = db.query(JobStatusHistory).filter(JobStatusHistory.job_id == job.job_id).all()
        for history in status_history:
            history_status = db.query(JobStatus).filter(JobStatus.job_status_id == history.job_status_id).first()
            job_data["status_history"].append({
                "history_id": history.job_status_history_id,
                "job_status": history_status.job_status if history_status else None,
                "date": history.date.isoformat() if history.date else None
            })
        
        quotes = db.query(Quote).filter(Quote.job_id == job.job_id).all()
        for quote in quotes:
            quote_data = {
                "quote_id": quote.quote_id,
                "quote_number": quote.quote_number,
                "date_created": quote.date_created.isoformat() if quote.date_created else None,
                "cost_excl_gst": float(quote.cost_excl_gst) if quote.cost_excl_gst else None,
                "cost_incl_gst": float(quote.cost_incl_gst) if quote.cost_incl_gst else None,
                "items": []
            }
            items = db.query(Item).filter(Item.quote_id == quote.quote_id).all()
            for item in items:
                product = db.query(Product).filter(Product.product_id == item.product_id).first()
                quote_data["items"].append({
                    "item_id": item.item_id,
                    "product_id": item.product_id,
                    "product_name": product.name if product else "Unknown Product",
                    "reference": item.reference,
                    "notes": item.notes,
                    "quantity": float(item.quantity),
                    "length": float(item.length) if item.length else None,
                    "height": float(item.height) if item.height else None,
                    "cost_excl_gst": float(item.cost_excl_gst) if item.cost_excl_gst else None,
                    "cost_incl_gst": float(item.cost_incl_gst) if item.cost_incl_gst else None
                })
            job_data["quotes"].append(quote_data)
        
        result.append(job_data)
    return result

@app.post("/api/jobs")
async def create_job(
    job: JobCreate,
    attachments: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    try:
        new_job = Job(
            reference=job.reference,
            project_id=job.project_id,
            client_id=job.client_id,
            billing_entity=job.billing_entity,
            po=job.po,
            date_created=job.date_created,
            contact_id=job.contact_id,
            staff_id=job.staff_id,
            job_status_id=job.job_status_id
        )
        db.add(new_job)
        db.flush()
        
        assets_info = []
        if attachments and DROPBOX_AVAILABLE:
            try:
                dropbox_service = get_dropbox_service()
                files_to_upload = []
                for file in attachments:
                    if file.filename:
                        file_content = await file.read()
                        files_to_upload.append({
                            "content": file_content,
                            "filename": file.filename
                        })
                if files_to_upload:
                    upload_results = dropbox_service.upload_multiple_files(files_to_upload, new_job.job_id)
                    assets_info = [{
                        "dropbox_path": r["dropbox_path"],
                        "dropbox_shared_url": r["dropbox_shared_url"]
                    } for r in upload_results]
                    new_job.assets = json.dumps(assets_info)
            except Exception as e:
                print(f"Error uploading job attachments: {str(e)}")
        
        db.commit()
        db.refresh(new_job)
        
        initial_history = JobStatusHistory(
            job_id=new_job.job_id,
            job_status_id=new_job.job_status_id,
            date=new_job.date_created or datetime.now().date()
        )
        db.add(initial_history)
        db.commit()
        
        return {
            "job_id": new_job.job_id,
            "reference": new_job.reference,
            "project_id": new_job.project_id,
            "client_id": new_job.client_id,
            "billing_entity": new_job.billing_entity,
            "po": new_job.po,
            "date_created": new_job.date_created.isoformat() if new_job.date_created else None,
            "contact_id": new_job.contact_id,
            "staff_id": new_job.staff_id,
            "job_status_id": new_job.job_status_id,
            "assets": assets_info
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/jobs/{job_id}")
async def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    try:
        job_obj = db.query(Job).filter(Job.job_id == job_id).first()
        if not job_obj:
            raise HTTPException(status_code=404, detail="Job not found")
        
        old_status = job_obj.job_status_id
        
        if job.reference is not None:
            job_obj.reference = job.reference
        if job.project_id is not None:
            job_obj.project_id = job.project_id
        if job.client_id is not None:
            job_obj.client_id = job.client_id
        if job.billing_entity is not None:
            job_obj.billing_entity = job.billing_entity
        if job.po is not None:
            job_obj.po = job.po
        if job.contact_id is not None:
            job_obj.contact_id = job.contact_id
        if job.staff_id is not None:
            job_obj.staff_id = job.staff_id
        if job.job_status_id is not None:
            job_obj.job_status_id = job.job_status_id
        
        if old_status != job_obj.job_status_id:
            new_history = JobStatusHistory(
                job_id=job_obj.job_id,
                job_status_id=job_obj.job_status_id,
                date=datetime.now().date()
            )
            db.add(new_history)
        
        db.commit()
        return {
            "job_id": job_obj.job_id,
            "reference": job_obj.reference,
            "project_id": job_obj.project_id,
            "client_id": job_obj.client_id,
            "billing_entity": job_obj.billing_entity,
            "po": job_obj.po,
            "date_created": job_obj.date_created.isoformat() if job_obj.date_created else None,
            "contact_id": job_obj.contact_id,
            "staff_id": job_obj.staff_id,
            "job_status_id": job_obj.job_status_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        db.delete(job)
        db.commit()
        return {"message": "Job deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Staff
@app.get("/api/staff")
async def get_staff(db: Session = Depends(get_db)):
    staff_members = db.query(Staff).all()
    result = []
    for staff_member in staff_members:
        assigned_jobs = db.query(Job).filter(Job.staff_id == staff_member.staff_id).all()
        jobs_data = []
        for job in assigned_jobs:
            client = db.query(Client).filter(Client.client_id == job.client_id).first()
            project = db.query(Project).filter(Project.project_id == job.project_id).first()
            job_status = db.query(JobStatus).filter(JobStatus.job_status_id == job.job_status_id).first()
            jobs_data.append({
                "job_id": job.job_id,
                "reference": job.reference,
                "client_name": client.name if client else None,
                "project_name": project.name if project else None,
                "status": job_status.job_status if job_status else None
            })
        
        result.append({
            "staff_id": staff_member.staff_id,
            "first_name": staff_member.first_name,
            "surname": staff_member.surname,
            "phone": staff_member.phone,
            "address": staff_member.address,
            "suburb": staff_member.suburb,
            "state": staff_member.state,
            "postcode": staff_member.postcode,
            "dob": staff_member.dob.isoformat() if staff_member.dob else None,
            "emergency_contact": staff_member.emergency_contact,
            "emergency_contact_number": staff_member.emergency_contact_number,
            "assigned_jobs": jobs_data
        })
    return result

@app.post("/api/staff")
async def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    try:
        new_staff = Staff(
            first_name=staff.first_name,
            surname=staff.surname,
            phone=staff.phone,
            address=staff.address,
            suburb=staff.suburb,
            state=staff.state,
            postcode=staff.postcode,
            dob=staff.dob,
            emergency_contact=staff.emergency_contact,
            emergency_contact_number=staff.emergency_contact_number
        )
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        return {
            "staff_id": new_staff.staff_id,
            "message": "Staff member created successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/staff/{staff_id}")
async def update_staff(staff_id: int, staff: StaffUpdate, db: Session = Depends(get_db)):
    try:
        staff_obj = db.query(Staff).filter(Staff.staff_id == staff_id).first()
        if not staff_obj:
            raise HTTPException(status_code=404, detail="Staff member not found")
        
        staff_obj.first_name = staff.first_name
        staff_obj.surname = staff.surname
        staff_obj.phone = staff.phone
        staff_obj.address = staff.address
        staff_obj.suburb = staff.suburb
        staff_obj.state = staff.state
        staff_obj.postcode = staff.postcode
        staff_obj.dob = staff.dob
        staff_obj.emergency_contact = staff.emergency_contact
        staff_obj.emergency_contact_number = staff.emergency_contact_number
        
        db.commit()
        return {"message": "Staff member updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/staff/{staff_id}")
async def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    try:
        staff_member = db.query(Staff).filter(Staff.staff_id == staff_id).first()
        if not staff_member:
            raise HTTPException(status_code=404, detail="Staff member not found")
        
        assigned_jobs = db.query(Job).filter(Job.staff_id == staff_id).count()
        if assigned_jobs > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete staff member. They have {assigned_jobs} assigned job(s)."
            )
        
        db.delete(staff_member)
        db.commit()
        return {"message": "Staff member deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Projects
@app.get("/api/projects")
async def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [{
        "project_id": project.project_id,
        "name": project.name,
        "address": project.address,
        "suburb": project.suburb,
        "state": project.state,
        "postcode": project.postcode,
        "date_created": project.date_created.isoformat() if project.date_created else None
    } for project in projects]

@app.post("/api/projects")
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        new_project = Project(
            name=project.name,
            address=project.address,
            suburb=project.suburb,
            state=project.state,
            postcode=project.postcode
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return {
            "project_id": new_project.project_id,
            "name": new_project.name,
            "address": new_project.address,
            "suburb": new_project.suburb,
            "state": new_project.state,
            "postcode": new_project.postcode,
            "date_created": new_project.date_created.isoformat() if new_project.date_created else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/projects/{project_id}")
async def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    try:
        project_obj = db.query(Project).filter(Project.project_id == project_id).first()
        if not project_obj:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_obj.name = project.name
        project_obj.address = project.address
        project_obj.suburb = project.suburb
        project_obj.state = project.state
        project_obj.postcode = project.postcode
        
        db.commit()
        return {
            "project_id": project_obj.project_id,
            "name": project_obj.name,
            "address": project_obj.address,
            "suburb": project_obj.suburb,
            "state": project_obj.state,
            "postcode": project_obj.postcode,
            "date_created": project_obj.date_created.isoformat() if project_obj.date_created else None
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        db.delete(project)
        db.commit()
        return {"message": "Project deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/clients/{client_id}/projects")
async def get_client_projects(client_id: int, db: Session = Depends(get_db)):
    projects = db.query(Project).join(Job).filter(Job.client_id == client_id).distinct().all()
    return [{
        "project_id": project.project_id,
        "name": project.name,
        "address": project.address,
        "suburb": project.suburb,
        "state": project.state,
        "postcode": project.postcode,
        "date_created": project.date_created.isoformat() if project.date_created else None
    } for project in projects]

# API Routes for Job Statuses
@app.get("/api/job-statuses")
async def get_job_statuses(db: Session = Depends(get_db)):
    statuses = db.query(JobStatus).all()
    return [{
        "job_status_id": status.job_status_id,
        "job_status": status.job_status
    } for status in statuses]

# API Routes for Items
@app.post("/api/items")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        new_item = Item(
            quote_id=item.quote_id,
            product_id=item.product_id,
            reference=item.reference,
            length=item.length,
            height=item.height,
            quantity=item.quantity,
            notes=item.notes,
            cost_excl_gst=item.cost_excl_gst,
            cost_incl_gst=item.cost_incl_gst
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {
            "item_id": new_item.item_id,
            "quote_id": new_item.quote_id,
            "product_id": new_item.product_id,
            "reference": new_item.reference,
            "length": float(new_item.length) if new_item.length else None,
            "height": float(new_item.height) if new_item.height else None,
            "quantity": float(new_item.quantity),
            "notes": new_item.notes,
            "cost_excl_gst": float(new_item.cost_excl_gst) if new_item.cost_excl_gst else None,
            "cost_incl_gst": float(new_item.cost_incl_gst) if new_item.cost_incl_gst else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/items")
async def get_items(quote_id: Optional[int] = None, db: Session = Depends(get_db)):
    if quote_id:
        items = db.query(Item).filter(Item.quote_id == quote_id).all()
    else:
        items = db.query(Item).all()
    
    return [{
        "item_id": item.item_id,
        "quote_id": item.quote_id,
        "product_id": item.product_id,
        "reference": item.reference,
        "notes": item.notes,
        "quantity": float(item.quantity),
        "length": float(item.length) if item.length else None,
        "height": float(item.height) if item.height else None,
        "cost_excl_gst": float(item.cost_excl_gst) if item.cost_excl_gst else None,
        "cost_incl_gst": float(item.cost_incl_gst) if item.cost_incl_gst else None
    } for item in items]

@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(Item).filter(Item.item_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        db.delete(item)
        db.commit()
        return {"message": "Item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Item Variables
@app.get("/api/item-variables")
async def get_item_variables(item_id: Optional[int] = None, db: Session = Depends(get_db)):
    if item_id:
        item_variables = db.query(ItemVariable).filter(ItemVariable.item_id == item_id).all()
    else:
        item_variables = db.query(ItemVariable).all()
    
    result = []
    for item_var in item_variables:
        item_var_data = {
            "item_variable_id": item_var.item_variable_id,
            "item_id": item_var.item_id,
            "product_variable_id": item_var.product_variable_id,
            "variable_option_id": None
        }
        item_var_option = db.query(ItemVariableOption).filter(
            ItemVariableOption.item_variable_id == item_var.item_variable_id
        ).first()
        if item_var_option:
            item_var_data["variable_option_id"] = item_var_option.variable_option_id
        result.append(item_var_data)
    return result

@app.post("/api/item-variables")
async def create_item_variable(item_var: ItemVariableCreate, db: Session = Depends(get_db)):
    try:
        new_item_variable = ItemVariable(
            item_id=item_var.item_id,
            product_variable_id=item_var.product_variable_id
        )
        db.add(new_item_variable)
        db.commit()
        db.refresh(new_item_variable)
        
        if item_var.variable_option_id:
            new_item_variable_option = ItemVariableOption(
                item_variable_id=new_item_variable.item_variable_id,
                variable_option_id=item_var.variable_option_id
            )
            db.add(new_item_variable_option)
            db.commit()
        
        return {
            "item_variable_id": new_item_variable.item_variable_id,
            "item_id": new_item_variable.item_id,
            "product_variable_id": new_item_variable.product_variable_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Product Variables (for quote page)
@app.get("/api/products/{product_id}/variables")
async def get_product_variables(product_id: int, db: Session = Depends(get_db)):
    variables = (
        db.query(ProductVariable, ProductProductVariable.display_order)
        .join(ProductProductVariable, ProductProductVariable.product_variable_id == ProductVariable.product_variable_id)
        .filter(ProductProductVariable.product_id == product_id)
        .order_by(ProductProductVariable.display_order)
        .all()
    )
    result = []
    for variable, display_order in variables:
        variable_data = {
            "product_variable_id": variable.product_variable_id,
            "name": variable.name,
            "display_order": display_order,
            "options": []
        }
        options = db.query(VariableOption).filter(VariableOption.product_variable_id == variable.product_variable_id).all()
        for option in options:
            variable_data["options"].append({
                "variable_option_id": option.variable_option_id,
                "name": option.name,
                "base_cost": float(option.base_cost) if option.base_cost else 0.0,
                "multiplier_cost": float(option.multiplier_cost) if option.multiplier_cost else 0.0
            })
        result.append(variable_data)
    return result

@app.post("/api/products/{product_id}/variables/{variable_id}")
async def assign_variable_to_product(product_id: int, variable_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        variable = db.query(ProductVariable).filter(ProductVariable.product_variable_id == variable_id).first()
        if not variable:
            raise HTTPException(status_code=404, detail="Variable not found")
        
        existing = db.query(ProductProductVariable).filter(
            ProductProductVariable.product_id == product_id,
            ProductProductVariable.product_variable_id == variable_id
        ).first()
        if existing:
            return {"message": "Variable already assigned to product"}
        
        max_order = (
            db.query(func.coalesce(func.max(ProductProductVariable.display_order), 0))
            .filter(ProductProductVariable.product_id == product_id)
            .scalar()
        ) or 0
        
        assignment = ProductProductVariable(
            product_id=product_id,
            product_variable_id=variable_id,
            display_order=max_order + 1
        )
        db.add(assignment)
        db.commit()
        
        return {
            "message": "Variable assigned successfully",
            "product_id": product_id,
            "product_variable_id": variable_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# API Routes for Variable Option Costs
@app.post("/api/variable-options/costs")
async def get_variable_option_costs(request: VariableOptionCostsRequest, db: Session = Depends(get_db)):
    if not request.option_ids:
        return []
    
    options = db.query(VariableOption).filter(VariableOption.variable_option_id.in_(request.option_ids)).all()
    return [{
        "variable_option_id": option.variable_option_id,
        "base_cost": float(option.base_cost),
        "multiplier_cost": float(option.multiplier_cost)
    } for option in options]

# API Routes for Quotes
@app.get("/api/quotes")
async def get_quotes(job_id: Optional[int] = None, db: Session = Depends(get_db)):
    if job_id:
        quotes = db.query(Quote).filter(Quote.job_id == job_id).all()
    else:
        quotes = db.query(Quote).all()
    
    return [{
        "quote_id": quote.quote_id,
        "quote_number": quote.quote_number,
        "job_id": quote.job_id,
        "date_created": quote.date_created.isoformat() if quote.date_created else None,
        "cost_excl_gst": float(quote.cost_excl_gst) if quote.cost_excl_gst else None,
        "cost_incl_gst": float(quote.cost_incl_gst) if quote.cost_incl_gst else None
    } for quote in quotes]

@app.get("/api/quotes/{quote_id}")
async def get_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.quote_id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    items = db.query(Item).filter(Item.quote_id == quote_id).all()
    items_data = []
    for item in items:
        item_data = {
            "item_id": item.item_id,
            "product_id": item.product_id,
            "reference": item.reference,
            "notes": item.notes,
            "quantity": float(item.quantity),
            "length": float(item.length) if item.length else None,
            "height": float(item.height) if item.height else None,
            "cost_excl_gst": float(item.cost_excl_gst) if item.cost_excl_gst else None,
            "cost_incl_gst": float(item.cost_incl_gst) if item.cost_incl_gst else None
        }
        product = db.query(Product).filter(Product.product_id == item.product_id).first()
        if product:
            item_data["product"] = {
                "product_id": product.product_id,
                "name": product.name,
                "product_category_id": product.product_category_id
            }
        items_data.append(item_data)
    
    return {
        "quote_id": quote.quote_id,
        "quote_number": quote.quote_number,
        "job_id": quote.job_id,
        "date_created": quote.date_created.isoformat() if quote.date_created else None,
        "cost_excl_gst": float(quote.cost_excl_gst) if quote.cost_excl_gst else None,
        "cost_incl_gst": float(quote.cost_incl_gst) if quote.cost_incl_gst else None,
        "items": items_data
    }

@app.post("/api/quotes")
async def create_quote(quote: QuoteCreate, db: Session = Depends(get_db)):
    try:
        if not quote.job_id:
            raise HTTPException(status_code=400, detail="job_id is required")
        
        quote_number = generate_quote_number(quote.job_id, db)
        
        new_quote = Quote(
            quote_number=quote_number,
            job_id=quote.job_id,
            date_created=quote.date_created or datetime.now().date(),
            cost_excl_gst=quote.cost_excl_gst or 0.0,
            cost_incl_gst=quote.cost_incl_gst or 0.0
        )
        db.add(new_quote)
        db.commit()
        db.refresh(new_quote)
        
        return {
            "quote_id": new_quote.quote_id,
            "quote_number": new_quote.quote_number,
            "job_id": new_quote.job_id,
            "date_created": new_quote.date_created.isoformat() if new_quote.date_created else None,
            "cost_excl_gst": float(new_quote.cost_excl_gst) if new_quote.cost_excl_gst else None,
            "cost_incl_gst": float(new_quote.cost_incl_gst) if new_quote.cost_incl_gst else None
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/quotes/{quote_id}")
async def update_quote(quote_id: int, quote: QuoteUpdate, db: Session = Depends(get_db)):
    try:
        quote_obj = db.query(Quote).filter(Quote.quote_id == quote_id).first()
        if not quote_obj:
            raise HTTPException(status_code=404, detail="Quote not found")
        
        if quote.cost_excl_gst is not None:
            quote_obj.cost_excl_gst = quote.cost_excl_gst
        if quote.cost_incl_gst is not None:
            quote_obj.cost_incl_gst = quote.cost_incl_gst
        
        db.commit()
        return {
            "quote_id": quote_obj.quote_id,
            "quote_number": quote_obj.quote_number,
            "job_id": quote_obj.job_id,
            "date_created": quote_obj.date_created.isoformat() if quote_obj.date_created else None,
            "cost_excl_gst": float(quote_obj.cost_excl_gst) if quote_obj.cost_excl_gst else None,
            "cost_incl_gst": float(quote_obj.cost_incl_gst) if quote_obj.cost_incl_gst else None
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Update job status
@app.put("/api/jobs/{job_id}/status")
async def update_job_status(job_id: int, status_update: JobStatusUpdate, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.job_status_id == 2 and status_update.job_status_id == 1:
            job.approved_quote = None
        
        job.job_status_id = status_update.job_status_id
        
        new_history = JobStatusHistory(
            job_id=job_id,
            job_status_id=status_update.job_status_id,
            date=datetime.now()
        )
        db.add(new_history)
        db.commit()
        
        return {"message": "Job status updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Update job address
@app.put("/api/jobs/{job_id}/address")
async def update_job_address(job_id: int, address_update: JobAddressUpdate, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if address_update.job_address is not None:
            job.job_address = address_update.job_address
        if address_update.suburb is not None:
            job.suburb = address_update.suburb
        if address_update.state is not None:
            job.state = address_update.state
        if address_update.postcode is not None:
            job.postcode = address_update.postcode
        
        db.commit()
        return {"message": "Job address updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Update job billing entity
@app.put("/api/jobs/{job_id}/billing")
async def update_job_billing_entity(job_id: int, billing_update: JobBillingUpdate, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job.billing_entity = billing_update.billing_entity
        db.commit()
        return {"message": "Job billing entity updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/billing")
async def create_billing_entity(billing: BillingCreate, db: Session = Depends(get_db)):
    try:
        if not billing.client_id:
            raise HTTPException(status_code=400, detail="Client ID is required")
        if not billing.entity:
            raise HTTPException(status_code=400, detail="Entity name is required")
        
        billing_entity = Billing(
            client_id=billing.client_id,
            entity=billing.entity,
            address=billing.address,
            suburb=billing.suburb,
            state=billing.state,
            postcode=billing.postcode
        )
        db.add(billing_entity)
        db.commit()
        
        return {
            "billing_id": billing_entity.billing_id,
            "entity": billing_entity.entity,
            "address": billing_entity.address,
            "suburb": billing_entity.suburb,
            "state": billing_entity.state,
            "postcode": billing_entity.postcode
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/jobs/{job_id}/approve-quote")
async def approve_quote(job_id: int, request: ApproveQuoteRequest, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if request.approved_quote:
            quote = db.query(Quote).filter(
                Quote.quote_id == request.approved_quote,
                Quote.job_id == job_id
            ).first()
            if not quote:
                raise HTTPException(status_code=400, detail="Quote not found or does not belong to this job")
        
        job.approved_quote = request.approved_quote
        
        if request.approved_quote:
            job.job_status_id = 2
            job.stage_id = 1
        
        db.commit()
        return {"message": "Quote approval updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Workflow API endpoints
@app.get("/api/stages")
async def get_stages(db: Session = Depends(get_db)):
    try:
        from models import ThroughputStage
        stages = db.query(ThroughputStage).order_by(ThroughputStage.stage_order).all()
        return [{
            "stage_id": stage.stage_id,
            "stage": stage.stage,
            "stage_order": stage.stage_order
        } for stage in stages]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/jobs/{job_id}/stage")
async def update_job_stage(job_id: int, stage_update: StageUpdate, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if stage_update.stage_id:
            from models import ThroughputStage
            stage = db.query(ThroughputStage).filter(ThroughputStage.stage_id == stage_update.stage_id).first()
            if not stage:
                raise HTTPException(status_code=400, detail="Stage not found")
        
        job.stage_id = stage_update.stage_id
        db.commit()
        return {"message": "Job stage updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/jobs/{job_id}/stage-due-date")
async def update_stage_due_date(job_id: int, due_date_update: StageDueDateUpdate, db: Session = Depends(get_db)):
    try:
        from models import ThroughputStageDate
        stage_date = db.query(ThroughputStageDate).filter(
            ThroughputStageDate.job_id == job_id,
            ThroughputStageDate.status_id == due_date_update.stage_id
        ).first()
        
        if stage_date:
            stage_date.due_date = due_date_update.due_date
        else:
            new_stage_date = ThroughputStageDate(
                job_id=job_id,
                status_id=due_date_update.stage_id,
                due_date=due_date_update.due_date
            )
            db.add(new_stage_date)
        
        db.commit()
        return {"message": "Stage due date updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        from models import ThroughputTask, ThroughputStatus
        
        max_order = db.query(ThroughputTask.task_order).filter(
            ThroughputTask.job_number == task.job_id,
            ThroughputTask.stage_id == task.stage_id
        ).order_by(ThroughputTask.task_order.desc()).first()
        
        next_order = (max_order[0] + 1) if max_order else 1
        
        default_status = db.query(ThroughputStatus).first()
        if not default_status:
            raise HTTPException(status_code=400, detail="No status found")
        
        new_task = ThroughputTask(
            task_name=task.task_name,
            job_number=task.job_id,
            item_id=task.item_id,
            stage_id=task.stage_id,
            status_id=default_status.status_id,
            task_order=next_order
        )
        db.add(new_task)
        db.commit()
        
        return {
            "message": "Task created successfully",
            "task_id": new_task.task_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/jobs/{job_id}/tasks")
async def get_job_tasks(job_id: int, stage_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        from models import ThroughputTask, ThroughputStatus
        
        query = db.query(ThroughputTask).filter(ThroughputTask.job_number == job_id)
        if stage_id:
            query = query.filter(ThroughputTask.stage_id == stage_id)
        
        tasks = query.order_by(ThroughputTask.task_order).all()
        
        statuses = db.query(ThroughputStatus).all()
        status_map = {s.status_id: s.status for s in statuses}
        
        return [{
            "task_id": task.task_id,
            "task_name": task.task_name,
            "job_number": task.job_number,
            "item_id": task.item_id,
            "stage_id": task.stage_id,
            "status_id": task.status_id,
            "status": status_map.get(task.status_id, "Unknown"),
            "task_order": task.task_order,
            "time_completed": task.time_completed.isoformat() if task.time_completed else None
        } for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/tasks/{task_id}/status")
async def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    try:
        from models import ThroughputTask
        
        task = db.query(ThroughputTask).filter(ThroughputTask.task_id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if status_update.completed:
            task.status_id = 2
            task.time_completed = datetime.now()
        else:
            task.status_id = 1
            task.time_completed = None
        
        db.commit()
        return {
            "message": "Task status updated successfully",
            "task_id": task.task_id,
            "status_id": task.status_id,
            "time_completed": task.time_completed.isoformat() if task.time_completed else None
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Delivery API Endpoints
@app.get("/api/bookings")
async def get_bookings(db: Session = Depends(get_db)):
    try:
        bookings = db.query(Booking).all()
        result = []
        for booking in bookings:
            booking_data = {
                "booking_id": booking.booking_id,
                "pickup_date": booking.pickup_date.isoformat() if booking.pickup_date else None,
                "pickup_time": booking.pickup_time.isoformat() if booking.pickup_time else None,
                "dropoff_date": booking.dropoff_date.isoformat() if booking.dropoff_date else None,
                "dropoff_time": booking.dropoff_time.isoformat() if booking.dropoff_time else None,
                "notes": booking.notes,
                "job_number": booking.job_number,
                "completion": booking.completion,
                "created": booking.created.isoformat() if booking.created else None,
                "pickup_complete": booking.pickup_complete.isoformat() if booking.pickup_complete else None,
                "dropoff_complete": booking.dropoff_complete.isoformat() if booking.dropoff_complete else None,
                "creator_id": booking.creator_id
            }
            
            if booking.pickup_address:
                booking_data["pickup_address"] = {
                    "address_id": booking.pickup_address.address_id,
                    "formatted_address": booking.pickup_address.formatted_address,
                    "suburb": booking.pickup_address.suburb
                }
            
            if booking.dropoff_address:
                booking_data["dropoff_address"] = {
                    "address_id": booking.dropoff_address.address_id,
                    "formatted_address": booking.dropoff_address.formatted_address,
                    "suburb": booking.dropoff_address.suburb
                }
            
            result.append(booking_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/upload-attachments")
async def upload_attachments(
    files: List[UploadFile] = File(...),
    booking_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if not files or all(not file.filename for file in files):
            raise HTTPException(status_code=400, detail="No files selected")
        
        if not DROPBOX_AVAILABLE:
            raise HTTPException(status_code=500, detail="Dropbox service not available")
        
        files_to_upload = []
        for file in files:
            if file.filename:
                file_content = await file.read()
                files_to_upload.append({
                    "content": file_content,
                    "filename": file.filename
                })
        
        if not files_to_upload:
            raise HTTPException(status_code=400, detail="No valid files to upload")
        
        dropbox_service = get_dropbox_service()
        upload_results = dropbox_service.upload_multiple_files(files_to_upload, booking_id)
        
        attachments = []
        for result in upload_results:
            attachment = Attachment(
                booking_id=booking_id,
                dropbox_path=result["dropbox_path"],
                dropbox_shared_url=result["dropbox_shared_url"],
                uploaded_by=1
            )
            db.add(attachment)
            attachments.append(attachment)
        
        db.commit()
        
        return {
            "message": f"Successfully uploaded {len(attachments)} files",
            "attachments": [{
                "attachment_id": att.attachment_id,
                "dropbox_path": att.dropbox_path,
                "dropbox_shared_url": att.dropbox_shared_url
            } for att in attachments]
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload files: {str(e)}")

@app.post("/api/bookings")
async def create_booking(
    booking: BookingCreate,
    attachments: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    try:
        pickup_address_id = None
        if booking.pickupAddress:
            pickup_address_details = None
            if booking.pickup_address_details:
                try:
                    pickup_address_details = json.loads(booking.pickup_address_details)
                except (json.JSONDecodeError, TypeError):
                    pickup_address_details = None
            
            if pickup_address_details:
                pickup_address = Address(
                    name=None,
                    google_place_id=pickup_address_details.get("google_place_id"),
                    formatted_address=pickup_address_details.get("formatted_address", booking.pickupAddress),
                    street_number=pickup_address_details.get("street_number"),
                    street_name=pickup_address_details.get("street_name"),
                    suburb=pickup_address_details.get("suburb"),
                    state=pickup_address_details.get("state"),
                    postcode=pickup_address_details.get("postcode"),
                    country=pickup_address_details.get("country"),
                    latitude=pickup_address_details.get("latitude"),
                    longitude=pickup_address_details.get("longitude")
                )
            else:
                pickup_address_parts = booking.pickupAddress.split(",")
                pickup_suburb = pickup_address_parts[-1].strip() if len(pickup_address_parts) > 1 else ""
                pickup_address = Address(
                    formatted_address=booking.pickupAddress,
                    suburb=pickup_suburb,
                    state="NSW",
                    postcode="",
                    country="Australia"
                )
            db.add(pickup_address)
            db.flush()
            pickup_address_id = pickup_address.address_id
        
        dropoff_address_id = None
        if booking.dropoffAddress:
            dropoff_address_details = None
            if booking.dropoff_address_details:
                try:
                    dropoff_address_details = json.loads(booking.dropoff_address_details)
                except (json.JSONDecodeError, TypeError):
                    dropoff_address_details = None
            
            if dropoff_address_details:
                dropoff_address = Address(
                    name=None,
                    google_place_id=dropoff_address_details.get("google_place_id"),
                    formatted_address=dropoff_address_details.get("formatted_address", booking.dropoffAddress),
                    street_number=dropoff_address_details.get("street_number"),
                    street_name=dropoff_address_details.get("street_name"),
                    suburb=dropoff_address_details.get("suburb"),
                    state=dropoff_address_details.get("state"),
                    postcode=dropoff_address_details.get("postcode"),
                    country=dropoff_address_details.get("country"),
                    latitude=dropoff_address_details.get("latitude"),
                    longitude=dropoff_address_details.get("longitude")
                )
            else:
                dropoff_address_parts = booking.dropoffAddress.split(",")
                dropoff_suburb = dropoff_address_parts[-1].strip() if len(dropoff_address_parts) > 1 else ""
                dropoff_address = Address(
                    formatted_address=booking.dropoffAddress,
                    suburb=dropoff_suburb,
                    state="NSW",
                    postcode="",
                    country="Australia"
                )
            db.add(dropoff_address)
            db.flush()
            dropoff_address_id = dropoff_address.address_id
        
        new_booking = Booking(
            pickup_address_id=pickup_address_id,
            pickup_date=booking.pickup_date,
            pickup_time=booking.pickup_time,
            dropoff_address_id=dropoff_address_id,
            dropoff_date=booking.dropoff_date,
            dropoff_time=booking.dropoff_time,
            creator_id=booking.creator_id or 1,
            notes=booking.notes,
            job_number=booking.job_number,
            completion=False
        )
        db.add(new_booking)
        db.flush()
        
        attachment_info = []
        if attachments and DROPBOX_AVAILABLE:
            try:
                dropbox_service = get_dropbox_service()
                files_to_upload = []
                for file in attachments:
                    if file.filename:
                        file_content = await file.read()
                        files_to_upload.append({
                            "content": file_content,
                            "filename": file.filename
                        })
                
                if files_to_upload:
                    upload_results = dropbox_service.upload_multiple_files(files_to_upload, new_booking.booking_id)
                    for result in upload_results:
                        attachment = Attachment(
                            booking_id=new_booking.booking_id,
                            dropbox_path=result["dropbox_path"],
                            dropbox_shared_url=result["dropbox_shared_url"],
                            uploaded_by=booking.creator_id or 1
                        )
                        db.add(attachment)
                        attachment_info.append({
                            "attachment_id": attachment.attachment_id,
                            "dropbox_path": attachment.dropbox_path,
                            "dropbox_shared_url": attachment.dropbox_shared_url
                        })
            except Exception as upload_error:
                print(f"Error uploading files: {str(upload_error)}")
        
        db.commit()
        return {
            "message": "Booking created successfully",
            "booking_id": new_booking.booking_id,
            "attachments": attachment_info
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/bookings/{booking_id}")
async def update_booking(booking_id: int, booking_update: BookingUpdate, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        if booking_update.completion is not None:
            booking.completion = booking_update.completion
        
        if booking_update.pickup_complete is not None:
            if booking_update.pickup_complete:
                if isinstance(booking_update.pickup_complete, str):
                    booking.pickup_complete = datetime.fromisoformat(booking_update.pickup_complete.replace("Z", "+00:00"))
                else:
                    booking.pickup_complete = booking_update.pickup_complete
            else:
                booking.pickup_complete = None
        
        if booking_update.dropoff_complete is not None:
            if booking_update.dropoff_complete:
                if isinstance(booking_update.dropoff_complete, str):
                    booking.dropoff_complete = datetime.fromisoformat(booking_update.dropoff_complete.replace("Z", "+00:00"))
                else:
                    booking.dropoff_complete = booking_update.dropoff_complete
            else:
                booking.dropoff_complete = None
        
        db.commit()
        return {
            "message": "Booking updated successfully",
            "booking_id": booking.booking_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    from config import HOST, PORT
    uvicorn.run(app, host=HOST, port=PORT)
