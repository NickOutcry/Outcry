"""
Job domain router - Project, Job, Quote, Item, JobStatus CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import SessionLocal
from models.job import (
    Project, Job, Quote, Item, ItemVariable, ItemVariableOption,
    JobStatus, JobStatusHistory
)
from models.client import Client, Contact, Billing
from models.staff import Staff
from models.product import Product
from schemas.job import (
    ProjectBase, ProjectCreate, ProjectRead,
    JobBase, JobCreate, JobRead,
    QuoteBase, QuoteCreate, QuoteRead,
    ItemBase, ItemCreate, ItemRead,
    ItemVariableBase, ItemVariableCreate, ItemVariableRead,
    ItemVariableOptionBase, ItemVariableOptionCreate, ItemVariableOptionRead,
    JobStatusBase, JobStatusCreate, JobStatusRead,
    JobStatusHistoryBase, JobStatusHistoryCreate, JobStatusHistoryRead
)
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["job"])


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# PROJECT ROUTES
# ============================================================================

@router.get("/projects", response_model=List[ProjectRead])
async def get_projects(db: Session = Depends(get_db)):
    """Get all projects"""
    projects = db.query(Project).all()
    return projects


@router.get("/projects/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a single project by ID"""
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/projects", response_model=ProjectRead, status_code=201)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
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
        return new_project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/projects/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    project: ProjectBase,
    db: Session = Depends(get_db)
):
    """Update an existing project"""
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
        db.refresh(project_obj)
        return project_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/projects/{project_id}", status_code=204)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project"""
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        db.delete(project)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/clients/{client_id}/projects", response_model=List[ProjectRead])
async def get_client_projects(client_id: int, db: Session = Depends(get_db)):
    """Get all projects for a specific client"""
    projects = db.query(Project).join(Job).filter(Job.client_id == client_id).distinct().all()
    return projects


# ============================================================================
# JOB STATUS ROUTES
# ============================================================================

@router.get("/job-statuses", response_model=List[JobStatusRead])
async def get_job_statuses(db: Session = Depends(get_db)):
    """Get all job statuses"""
    statuses = db.query(JobStatus).all()
    return statuses


@router.get("/job-statuses/{status_id}", response_model=JobStatusRead)
async def get_job_status(status_id: int, db: Session = Depends(get_db)):
    """Get a single job status by ID"""
    status = db.query(JobStatus).filter(JobStatus.job_status_id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Job status not found")
    return status


@router.post("/job-statuses", response_model=JobStatusRead, status_code=201)
async def create_job_status(status: JobStatusCreate, db: Session = Depends(get_db)):
    """Create a new job status"""
    try:
        new_status = JobStatus(job_status=status.job_status)
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return new_status
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# JOB ROUTES
# ============================================================================

@router.get("/jobs", response_model=List[JobRead])
async def get_jobs(db: Session = Depends(get_db)):
    """Get all jobs"""
    jobs = db.query(Job).all()
    return jobs


@router.get("/jobs/{job_id}", response_model=JobRead)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a single job by ID"""
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/jobs", response_model=JobRead, status_code=201)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job"""
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
        
        # Create initial status history
        initial_history = JobStatusHistory(
            job_id=new_job.job_id,
            job_status_id=new_job.job_status_id,
            date=new_job.date_created or datetime.now().date()
        )
        db.add(initial_history)
        db.commit()
        db.refresh(new_job)
        return new_job
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/jobs/{job_id}", response_model=JobRead)
async def update_job(
    job_id: int,
    job: JobBase,
    db: Session = Depends(get_db)
):
    """Update an existing job"""
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
        
        # Create status history entry if status changed
        if job.job_status_id is not None and old_status != job_obj.job_status_id:
            new_history = JobStatusHistory(
                job_id=job_obj.job_id,
                job_status_id=job_obj.job_status_id,
                date=datetime.now().date()
            )
            db.add(new_history)
        
        db.commit()
        db.refresh(job_obj)
        return job_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/jobs/{job_id}", status_code=204)
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete a job"""
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        db.delete(job)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# QUOTE ROUTES
# ============================================================================

def generate_quote_number(job_id: int, db: Session) -> str:
    """Generate a unique quote number for a job"""
    existing_quotes = db.query(Quote).filter(Quote.job_id == job_id).count()
    next_quote_number = existing_quotes + 1
    return f"{job_id}-{next_quote_number:03d}"


@router.get("/quotes", response_model=List[QuoteRead])
async def get_quotes(job_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all quotes, optionally filtered by job_id"""
    query = db.query(Quote)
    if job_id:
        query = query.filter(Quote.job_id == job_id)
    quotes = query.all()
    return quotes


@router.get("/quotes/{quote_id}", response_model=QuoteRead)
async def get_quote(quote_id: int, db: Session = Depends(get_db)):
    """Get a single quote by ID with items"""
    quote = db.query(Quote).filter(Quote.quote_id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    items = db.query(Item).filter(Item.quote_id == quote_id).all()
    items_data = []
    for item in items:
        items_data.append({
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
        })
    
    return {
        "quote_id": quote.quote_id,
        "quote_number": quote.quote_number,
        "job_id": quote.job_id,
        "date_created": quote.date_created,
        "cost_excl_gst": float(quote.cost_excl_gst) if quote.cost_excl_gst else None,
        "cost_incl_gst": float(quote.cost_incl_gst) if quote.cost_incl_gst else None,
        "items": items_data
    }


@router.post("/quotes", response_model=QuoteRead, status_code=201)
async def create_quote(quote: QuoteCreate, db: Session = Depends(get_db)):
    """Create a new quote"""
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
        return new_quote
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/quotes/{quote_id}", response_model=QuoteRead)
async def update_quote(
    quote_id: int,
    quote: QuoteBase,
    db: Session = Depends(get_db)
):
    """Update an existing quote"""
    try:
        quote_obj = db.query(Quote).filter(Quote.quote_id == quote_id).first()
        if not quote_obj:
            raise HTTPException(status_code=404, detail="Quote not found")
        
        if quote.cost_excl_gst is not None:
            quote_obj.cost_excl_gst = quote.cost_excl_gst
        if quote.cost_incl_gst is not None:
            quote_obj.cost_incl_gst = quote.cost_incl_gst
        
        db.commit()
        db.refresh(quote_obj)
        return quote_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# ITEM ROUTES
# ============================================================================

@router.get("/items", response_model=List[ItemRead])
async def get_items(quote_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all items, optionally filtered by quote_id"""
    query = db.query(Item)
    if quote_id:
        query = query.filter(Item.quote_id == quote_id)
    items = query.all()
    return items


@router.get("/items/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a single item by ID"""
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/items", response_model=ItemRead, status_code=201)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item"""
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
        return new_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item"""
    try:
        item = db.query(Item).filter(Item.item_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        db.delete(item)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# ITEM VARIABLE ROUTES
# ============================================================================

@router.get("/item-variables", response_model=List[ItemVariableRead])
async def get_item_variables(
    item_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all item variables, optionally filtered by item_id"""
    query = db.query(ItemVariable)
    if item_id:
        query = query.filter(ItemVariable.item_id == item_id)
    item_variables = query.all()
    return item_variables


@router.post("/item-variables", response_model=ItemVariableRead, status_code=201)
async def create_item_variable(
    item_variable: ItemVariableCreate,
    db: Session = Depends(get_db)
):
    """Create a new item variable"""
    try:
        new_item_variable = ItemVariable(
            item_id=item_variable.item_id,
            product_variable_id=item_variable.product_variable_id
        )
        db.add(new_item_variable)
        db.commit()
        db.refresh(new_item_variable)
        
        if item_variable.variable_option_id:
            new_item_variable_option = ItemVariableOption(
                item_variable_id=new_item_variable.item_variable_id,
                variable_option_id=item_variable.variable_option_id
            )
            db.add(new_item_variable_option)
            db.commit()
        
        return new_item_variable
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))



# ============================================================================
# TEST ENDPOINT
# ============================================================================

@router.get("/job/test", response_class=JSONResponse)
async def test_job_connection(db: Session = Depends(get_db)):
    """
    Test endpoint to verify database connection and models.
    Returns the first record from Project, Job, and Quote tables.
    """
    result = {
        "status": "success",
        "message": "Database connection and models are working",
        "data": {}
    }
    
    try:
        # Test Project table
        first_project = db.query(Project).first()
        if first_project:
            result["data"]["project"] = {
                "project_id": first_project.project_id,
                "name": first_project.name,
                "address": first_project.address,
                "suburb": first_project.suburb,
                "state": first_project.state
            }
        else:
            result["data"]["project"] = None
        
        # Test Job table
        first_job = db.query(Job).first()
        if first_job:
            result["data"]["job"] = {
                "job_id": first_job.job_id,
                "reference": first_job.reference,
                "project_id": first_job.project_id,
                "client_id": first_job.client_id,
                "contact_id": first_job.contact_id,
                "staff_id": first_job.staff_id
            }
        else:
            result["data"]["job"] = None
        
        # Test Quote table
        first_quote = db.query(Quote).first()
        if first_quote:
            result["data"]["quote"] = {
                "quote_id": first_quote.quote_id,
                "quote_number": first_quote.quote_number,
                "job_id": first_quote.job_id,
                "cost_excl_gst": first_quote.cost_excl_gst,
                "cost_incl_gst": first_quote.cost_incl_gst
            }
        else:
            result["data"]["quote"] = None
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}",
            "data": {}
        }
