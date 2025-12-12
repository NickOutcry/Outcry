"""
Pydantic schemas for Staff domain models
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date


# Staff Schemas
class StaffBase(BaseModel):
    first_name: str
    surname: str
    phone: Optional[str] = None
    address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None
    dob: Optional[date] = None
    emergency_contact: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    email: Optional[str] = None


class StaffCreate(StaffBase):
    pass


class StaffRead(StaffBase):
    staff_id: int
    
    class Config:
        from_attributes = True

