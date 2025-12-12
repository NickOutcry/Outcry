"""
Staff domain router - Staff CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models.staff import Staff
from models.job import Job, Project
from models.client import Client
from models.job import JobStatus
from schemas.staff import (
    StaffBase, StaffCreate, StaffRead
)
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["staff"])


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# STAFF ROUTES
# ============================================================================

@router.get("/staff", response_model=List[StaffRead])
async def get_staff(db: Session = Depends(get_db)):
    """Get all staff members with their assigned jobs"""
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
        
        staff_data = {
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
            "email": staff_member.email,
            "assigned_jobs": jobs_data
        }
        result.append(staff_data)
    return result


@router.get("/staff/{staff_id}", response_model=StaffRead)
async def get_staff_member(staff_id: int, db: Session = Depends(get_db)):
    """Get a single staff member by ID"""
    staff_member = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff_member


@router.post("/staff", response_model=StaffRead, status_code=201)
async def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    """Create a new staff member"""
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
            emergency_contact_number=staff.emergency_contact_number,
            email=staff.email
        )
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        return new_staff
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/staff/{staff_id}", response_model=StaffRead)
async def update_staff(
    staff_id: int,
    staff: StaffBase,
    db: Session = Depends(get_db)
):
    """Update an existing staff member"""
    try:
        staff_member = db.query(Staff).filter(Staff.staff_id == staff_id).first()
        if not staff_member:
            raise HTTPException(status_code=404, detail="Staff member not found")
        
        staff_member.first_name = staff.first_name
        staff_member.surname = staff.surname
        staff_member.phone = staff.phone
        staff_member.address = staff.address
        staff_member.suburb = staff.suburb
        staff_member.state = staff.state
        staff_member.postcode = staff.postcode
        staff_member.dob = staff.dob
        staff_member.emergency_contact = staff.emergency_contact
        staff_member.emergency_contact_number = staff.emergency_contact_number
        staff_member.email = staff.email
        
        db.commit()
        db.refresh(staff_member)
        return staff_member
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/staff/{staff_id}", status_code=204)
async def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    """Delete a staff member"""
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
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))



# ============================================================================
# TEST ENDPOINT
# ============================================================================

@router.get("/staff/test", response_class=JSONResponse)
async def test_staff_connection(db: Session = Depends(get_db)):
    """
    Test endpoint to verify database connection and models.
    Returns the first record from Staff table.
    """
    try:
        first_staff = db.query(Staff).first()
        if first_staff:
            return {
                "status": "success",
                "message": "Database connection and models are working",
                "data": {
                    "staff_id": first_staff.staff_id,
                    "first_name": first_staff.first_name,
                    "surname": first_staff.surname,
                    "phone": first_staff.phone,
                    "address": first_staff.address,
                    "suburb": first_staff.suburb,
                    "state": first_staff.state,
                    "postcode": first_staff.postcode,
                    "email": first_staff.email
                }
            }
        else:
            return {
                "status": "success",
                "message": "Database connection working, but no staff records found",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}",
            "data": None
        }
