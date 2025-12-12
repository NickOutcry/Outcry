"""
Pydantic schemas for Client domain models
"""
from pydantic import BaseModel
from typing import Optional


# Client Schemas
class ClientBase(BaseModel):
    name: str
    address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    client_id: int
    
    class Config:
        from_attributes = True


# Contact Schemas
class ContactBase(BaseModel):
    first_name: str
    surname: str
    email: Optional[str] = None
    phone: Optional[str] = None
    client_id: int


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    contact_id: int
    
    class Config:
        from_attributes = True


# Billing Schemas
class BillingBase(BaseModel):
    entity: str
    address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None
    client_id: int


class BillingCreate(BillingBase):
    pass


class BillingRead(BillingBase):
    billing_id: int
    
    class Config:
        from_attributes = True

