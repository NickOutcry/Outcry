"""
Delivery domain router - Address, Booking, Attachment CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, time

from database import SessionLocal
from models.delivery import Address, Booking, Attachment
from schemas.delivery import (
    AddressBase, AddressCreate, AddressRead,
    BookingBase, BookingCreate, BookingRead,
    AttachmentBase, AttachmentCreate, AttachmentRead
)
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["delivery"])


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# ADDRESS ROUTES
# ============================================================================

@router.get("/addresses", response_model=List[AddressRead])
async def get_addresses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all addresses"""
    addresses = db.query(Address).offset(skip).limit(limit).all()
    return addresses


@router.get("/addresses/{address_id}", response_model=AddressRead)
async def get_address(address_id: int, db: Session = Depends(get_db)):
    """Get a single address by ID"""
    address = db.query(Address).filter(Address.address_id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.post("/addresses", response_model=AddressRead, status_code=201)
async def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    """Create a new address"""
    db_address = Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


@router.put("/addresses/{address_id}", response_model=AddressRead)
async def update_address(
    address_id: int,
    address: AddressBase,
    db: Session = Depends(get_db)
):
    """Update an existing address"""
    db_address = db.query(Address).filter(Address.address_id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    for key, value in address.model_dump(exclude_unset=True).items():
        setattr(db_address, key, value)
    
    db.commit()
    db.refresh(db_address)
    return db_address


@router.delete("/addresses/{address_id}", status_code=204)
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    """Delete an address"""
    db_address = db.query(Address).filter(Address.address_id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    db.delete(db_address)
    db.commit()
    return None


# ============================================================================
# BOOKING ROUTES
# ============================================================================

@router.get("/bookings", response_model=List[BookingRead])
async def get_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all bookings"""
    bookings = db.query(Booking).offset(skip).limit(limit).all()
    return bookings


@router.get("/bookings/{booking_id}", response_model=BookingRead)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a single booking by ID"""
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/bookings", response_model=BookingRead, status_code=201)
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking"""
    db_booking = Booking(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.put("/bookings/{booking_id}", response_model=BookingRead)
async def update_booking(
    booking_id: int,
    booking: BookingBase,
    db: Session = Depends(get_db)
):
    """Update an existing booking"""
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    for key, value in booking.model_dump(exclude_unset=True).items():
        setattr(db_booking, key, value)
    
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.delete("/bookings/{booking_id}", status_code=204)
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Delete a booking"""
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(db_booking)
    db.commit()
    return None


# ============================================================================
# ATTACHMENT ROUTES
# ============================================================================

@router.get("/attachments", response_model=List[AttachmentRead])
async def get_attachments(
    skip: int = 0,
    limit: int = 100,
    booking_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all attachments, optionally filtered by booking_id"""
    query = db.query(Attachment)
    if booking_id is not None:
        query = query.filter(Attachment.booking_id == booking_id)
    attachments = query.offset(skip).limit(limit).all()
    return attachments


@router.get("/attachments/{attachment_id}", response_model=AttachmentRead)
async def get_attachment(attachment_id: int, db: Session = Depends(get_db)):
    """Get a single attachment by ID"""
    attachment = db.query(Attachment).filter(Attachment.attachment_id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return attachment


@router.post("/attachments", response_model=AttachmentRead, status_code=201)
async def create_attachment(attachment: AttachmentCreate, db: Session = Depends(get_db)):
    """Create a new attachment"""
    db_attachment = Attachment(**attachment.model_dump())
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


@router.put("/attachments/{attachment_id}", response_model=AttachmentRead)
async def update_attachment(
    attachment_id: int,
    attachment: AttachmentBase,
    db: Session = Depends(get_db)
):
    """Update an existing attachment"""
    db_attachment = db.query(Attachment).filter(Attachment.attachment_id == attachment_id).first()
    if not db_attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    for key, value in attachment.model_dump(exclude_unset=True).items():
        setattr(db_attachment, key, value)
    
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


@router.delete("/attachments/{attachment_id}", status_code=204)
async def delete_attachment(attachment_id: int, db: Session = Depends(get_db)):
    """Delete an attachment"""
    db_attachment = db.query(Attachment).filter(Attachment.attachment_id == attachment_id).first()
    if not db_attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    db.delete(db_attachment)
    db.commit()
    return None


# ============================================================================
# TEST ENDPOINT
# ============================================================================

@router.get("/delivery/test", response_class=JSONResponse)
async def test_delivery_connection(db: Session = Depends(get_db)):
    """
    Test endpoint to verify database connection and models.
    Returns the first record from Address, Booking, and Attachment tables.
    """
    result = {
        "status": "success",
        "message": "Database connection and models are working",
        "data": {}
    }
    
    try:
        # Test Address table
        first_address = db.query(Address).first()
        if first_address:
            result["data"]["address"] = {
                "address_id": first_address.address_id,
                "name": first_address.name,
                "formatted_address": first_address.formatted_address,
                "suburb": first_address.suburb,
                "state": first_address.state,
                "postcode": first_address.postcode
            }
        else:
            result["data"]["address"] = None
        
        # Test Booking table
        first_booking = db.query(Booking).first()
        if first_booking:
            result["data"]["booking"] = {
                "booking_id": first_booking.booking_id,
                "pickup_date": first_booking.pickup_date.isoformat() if first_booking.pickup_date else None,
                "dropoff_date": first_booking.dropoff_date.isoformat() if first_booking.dropoff_date else None,
                "completion": first_booking.completion,
                "job_number": first_booking.job_number
            }
        else:
            result["data"]["booking"] = None
        
        # Test Attachment table
        first_attachment = db.query(Attachment).first()
        if first_attachment:
            result["data"]["attachment"] = {
                "attachment_id": first_attachment.attachment_id,
                "booking_id": first_attachment.booking_id,
                "dropbox_path": first_attachment.dropbox_path,
                "uploaded_by": first_attachment.uploaded_by
            }
        else:
            result["data"]["attachment"] = None
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}",
            "data": {}
        }

