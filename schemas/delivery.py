"""
Pydantic schemas for Delivery domain models
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time
from decimal import Decimal


# Address Schemas
class AddressBase(BaseModel):
    name: Optional[str] = None
    google_place_id: Optional[str] = None
    formatted_address: Optional[str] = None
    street_number: Optional[str] = None
    street_name: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    address_id: int
    
    class Config:
        from_attributes = True


# Booking Schemas
class BookingBase(BaseModel):
    pickup_address_id: Optional[int] = None
    pickup_date: date
    pickup_time: Optional[time] = None
    dropoff_address_id: Optional[int] = None
    dropoff_date: date
    dropoff_time: Optional[time] = None
    creator_id: int
    notes: Optional[str] = None
    attachments: Optional[int] = None
    job_number: Optional[str] = None
    pickup_complete: Optional[datetime] = None
    dropoff_complete: Optional[datetime] = None
    created: Optional[datetime] = None
    completion: bool = False


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    booking_id: int
    
    class Config:
        from_attributes = True


# Attachment Schemas
class AttachmentBase(BaseModel):
    booking_id: Optional[int] = None
    dropbox_path: Optional[str] = None
    dropbox_shared_url: Optional[str] = None
    uploaded_by: Optional[int] = None
    uploaded_at: Optional[datetime] = None


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentRead(AttachmentBase):
    attachment_id: int
    
    class Config:
        from_attributes = True

