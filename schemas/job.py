"""
Pydantic schemas for Job domain models
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal


# Project Schemas
class ProjectBase(BaseModel):
    name: str
    address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None
    date_created: Optional[date] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    project_id: int
    
    class Config:
        from_attributes = True


# JobStatus Schemas
class JobStatusBase(BaseModel):
    job_status: str


class JobStatusCreate(JobStatusBase):
    pass


class JobStatusRead(JobStatusBase):
    job_status_id: int
    
    class Config:
        from_attributes = True


# Job Schemas
class JobBase(BaseModel):
    reference: str
    project_id: int
    client_id: int
    billing_entity: Optional[int] = None
    po: Optional[str] = None
    date_created: Optional[date] = None
    contact_id: int
    staff_id: int
    job_status_id: Optional[int] = None
    job_address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None
    approved_quote: Optional[int] = None
    stage_id: Optional[int] = None
    assets: Optional[str] = None


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    job_id: int
    
    class Config:
        from_attributes = True


# JobStatusHistory Schemas
class JobStatusHistoryBase(BaseModel):
    job_id: int
    job_status_id: int
    date: Optional[date] = None


class JobStatusHistoryCreate(JobStatusHistoryBase):
    pass


class JobStatusHistoryRead(JobStatusHistoryBase):
    job_status_history_id: int
    
    class Config:
        from_attributes = True


# Quote Schemas
class QuoteBase(BaseModel):
    quote_number: str
    job_id: int
    date_created: Optional[date] = None
    cost_excl_gst: Optional[float] = None
    cost_incl_gst: Optional[float] = None


class QuoteCreate(QuoteBase):
    pass


class QuoteRead(QuoteBase):
    quote_id: int
    
    class Config:
        from_attributes = True


# Item Schemas
class ItemBase(BaseModel):
    quote_id: int
    product_id: int
    reference: str = ''
    notes: Optional[str] = None
    quantity: float
    length: Optional[Decimal] = None
    height: Optional[Decimal] = None
    cost_excl_gst: Optional[float] = None
    cost_incl_gst: Optional[float] = None


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    item_id: int
    
    class Config:
        from_attributes = True


# ItemVariable Schemas
class ItemVariableBase(BaseModel):
    item_id: int
    product_variable_id: int


class ItemVariableCreate(ItemVariableBase):
    pass


class ItemVariableRead(ItemVariableBase):
    item_variable_id: int
    
    class Config:
        from_attributes = True


# ItemVariableOption Schemas
class ItemVariableOptionBase(BaseModel):
    item_variable_id: int
    variable_option_id: int


class ItemVariableOptionCreate(ItemVariableOptionBase):
    pass


class ItemVariableOptionRead(ItemVariableOptionBase):
    item_variable_option_id: int
    
    class Config:
        from_attributes = True

