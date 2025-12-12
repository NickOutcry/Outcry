"""
Pydantic schemas for request/response validation
Organized by domain to match models/ folder structure
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime, time


# ============================================================================
# CLIENT DOMAIN SCHEMAS
# ============================================================================

# Client Schemas
class ClientBase(BaseModel):
    name: str
    address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientRead(ClientBase):
    client_id: int
    
    class Config:
        from_attributes = True

class ClientResponse(ClientRead):
    contacts: List['ContactRead'] = []
    billing: List['BillingRead'] = []
    
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

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

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

class BillingUpdate(BaseModel):
    entity: Optional[str] = None
    address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None

class BillingRead(BillingBase):
    billing_id: int
    
    class Config:
        from_attributes = True


# ============================================================================
# PRODUCT DOMAIN SCHEMAS
# ============================================================================

# ProductCategory Schemas
class ProductCategoryBase(BaseModel):
    name: str

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryRead(ProductCategoryBase):
    product_category_id: int
    
    class Config:
        from_attributes = True


# MeasureType Schemas
class MeasureTypeBase(BaseModel):
    measure_type: str

class MeasureTypeCreate(MeasureTypeBase):
    pass

class MeasureTypeRead(MeasureTypeBase):
    measure_type_id: int
    
    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    product_category_id: int
    measure_type_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductRead(ProductBase):
    product_id: int
    
    class Config:
        from_attributes = True

class ProductResponse(ProductRead):
    base_cost: float = 0.0
    multiplier_cost: float = 0.0
    category_name: Optional[str] = None
    measure_type_name: Optional[str] = None
    variables: List['ProductVariableResponse'] = []
    
    class Config:
        from_attributes = True


# ProductVariable Schemas
class ProductVariableBase(BaseModel):
    name: str
    data_type: str

class ProductVariableCreate(ProductVariableBase):
    product_id: Optional[int] = None
    display_order: Optional[int] = None

class ProductVariableUpdate(ProductVariableBase):
    pass

class ProductVariableRead(ProductVariableBase):
    product_variable_id: int
    
    class Config:
        from_attributes = True

class VariableOptionResponse(BaseModel):
    variable_option_id: int
    name: str
    base_cost: float
    multiplier_cost: float
    
    class Config:
        from_attributes = True

class ProductVariableResponse(ProductVariableRead):
    base_cost: float = 0.0
    multiplier_cost: float = 0.0
    product_ids: List[int] = []
    options: List[VariableOptionResponse] = []
    
    class Config:
        from_attributes = True


# VariableOption Schemas
class VariableOptionBase(BaseModel):
    name: str
    base_cost: float
    multiplier_cost: float
    product_variable_id: int

class VariableOptionCreate(VariableOptionBase):
    pass

class VariableOptionUpdate(BaseModel):
    name: str
    base_cost: float
    multiplier_cost: float

class VariableOptionRead(VariableOptionBase):
    variable_option_id: int
    
    class Config:
        from_attributes = True


# ProductProductVariable Schemas (Join Table)
class ProductProductVariableBase(BaseModel):
    product_id: int
    product_variable_id: int
    display_order: Optional[int] = None

class ProductProductVariableCreate(ProductProductVariableBase):
    pass

class ProductProductVariableRead(ProductProductVariableBase):
    product_product_variable: int
    
    class Config:
        from_attributes = True


# ============================================================================
# STAFF DOMAIN SCHEMAS
# ============================================================================

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

class StaffUpdate(StaffBase):
    pass

class StaffRead(StaffBase):
    staff_id: int
    
    class Config:
        from_attributes = True

class StaffJobResponse(BaseModel):
    job_id: int
    reference: str
    client_name: Optional[str] = None
    project_name: Optional[str] = None
    status: Optional[str] = None

class StaffResponse(StaffRead):
    assigned_jobs: List[StaffJobResponse] = []
    
    class Config:
        from_attributes = True


# ============================================================================
# JOB DOMAIN SCHEMAS
# ============================================================================

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    project_id: int
    date_created: Optional[date] = None
    
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

class JobStatusHistoryResponse(JobStatusHistoryRead):
    job_status: Optional[str] = None


# Job Schemas
class JobBase(BaseModel):
    reference: str
    project_id: int
    client_id: int
    contact_id: int
    staff_id: int
    job_status_id: int
    billing_entity: Optional[int] = None
    po: Optional[str] = None
    date_created: Optional[date] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    reference: Optional[str] = None
    project_id: Optional[int] = None
    client_id: Optional[int] = None
    billing_entity: Optional[int] = None
    po: Optional[str] = None
    contact_id: Optional[int] = None
    staff_id: Optional[int] = None
    job_status_id: Optional[int] = None

class JobRead(JobBase):
    job_id: int
    job_address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None
    approved_quote: Optional[int] = None
    stage_id: Optional[int] = None
    assets: Optional[str] = None
    
    class Config:
        from_attributes = True

class QuoteItemResponse(BaseModel):
    item_id: int
    product_id: int
    product_name: str
    reference: str
    notes: Optional[str] = None
    quantity: float
    length: Optional[float] = None
    height: Optional[float] = None
    cost_excl_gst: Optional[float] = None
    cost_incl_gst: Optional[float] = None

class QuoteResponse(BaseModel):
    quote_id: int
    quote_number: str
    date_created: Optional[date] = None
    cost_excl_gst: Optional[float] = None
    cost_incl_gst: Optional[float] = None
    items: List[QuoteItemResponse] = []

class JobResponse(JobRead):
    stage_due_date: Optional[date] = None
    client_name: Optional[str] = None
    project_name: Optional[str] = None
    contact_name: Optional[str] = None
    staff_name: Optional[str] = None
    staff_first_name: Optional[str] = None
    staff_surname: Optional[str] = None
    staff_email: Optional[str] = None
    staff_phone: Optional[str] = None
    billing_entity_name: Optional[str] = None
    billing_address: Optional[str] = None
    billing_suburb: Optional[str] = None
    billing_state: Optional[str] = None
    billing_postcode: Optional[int] = None
    billing_entities: List[BillingRead] = []
    job_status: Optional[str] = None
    status_history: List[JobStatusHistoryResponse] = []
    quotes: List[QuoteResponse] = []


# Quote Schemas
class QuoteBase(BaseModel):
    job_id: int
    date_created: Optional[date] = None
    cost_excl_gst: Optional[float] = 0.0
    cost_incl_gst: Optional[float] = 0.0

class QuoteCreate(QuoteBase):
    pass

class QuoteUpdate(BaseModel):
    cost_excl_gst: Optional[float] = None
    cost_incl_gst: Optional[float] = None

class QuoteRead(QuoteBase):
    quote_id: int
    quote_number: str
    
    class Config:
        from_attributes = True

class QuoteDetailResponse(QuoteRead):
    items: List['ItemRead'] = []


# Item Schemas
class ItemBase(BaseModel):
    quote_id: int
    product_id: int
    reference: Optional[str] = ""
    notes: Optional[str] = None
    quantity: float
    length: Optional[float] = None
    height: Optional[float] = None
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
    variable_option_id: Optional[int] = None

class ItemVariableRead(ItemVariableBase):
    item_variable_id: int
    
    class Config:
        from_attributes = True

class ItemVariableResponse(ItemVariableRead):
    variable_option_id: Optional[int] = None
    
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


# ============================================================================
# WORKFLOW DOMAIN SCHEMAS
# ============================================================================

# ThroughputStatus Schemas
class ThroughputStatusBase(BaseModel):
    status: str

class ThroughputStatusCreate(ThroughputStatusBase):
    pass

class ThroughputStatusRead(ThroughputStatusBase):
    status_id: int
    
    class Config:
        from_attributes = True


# ThroughputStage Schemas
class ThroughputStageBase(BaseModel):
    stage: str
    stage_order: int

class ThroughputStageCreate(ThroughputStageBase):
    pass

class ThroughputStageRead(ThroughputStageBase):
    stage_id: int
    
    class Config:
        from_attributes = True

class StageResponse(ThroughputStageRead):
    pass


# ThroughputTask Schemas
class ThroughputTaskBase(BaseModel):
    task_name: str
    job_number: int
    item_id: Optional[int] = None
    stage_id: int
    status_id: int
    task_order: int

class ThroughputTaskCreate(ThroughputTaskBase):
    pass

class ThroughputTaskRead(ThroughputTaskBase):
    task_id: int
    time_completed: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TaskResponse(ThroughputTaskRead):
    status: str


# ThroughputStageDate Schemas
class ThroughputStageDateBase(BaseModel):
    job_id: int
    status_id: int
    due_date: date

class ThroughputStageDateCreate(ThroughputStageDateBase):
    pass

class ThroughputStageDateRead(ThroughputStageDateBase):
    stage_date_id: int
    
    class Config:
        from_attributes = True

class StageDueDateUpdate(BaseModel):
    stage_id: int
    due_date: date

class StageUpdate(BaseModel):
    stage_id: Optional[int] = None

class TaskCreate(BaseModel):
    task_name: str
    job_id: int
    item_id: Optional[int] = None
    stage_id: int

class TaskStatusUpdate(BaseModel):
    completed: bool


# ============================================================================
# DELIVERY DOMAIN SCHEMAS
# ============================================================================

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
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AddressCreate(AddressBase):
    pass

class AddressRead(AddressBase):
    address_id: int
    
    class Config:
        from_attributes = True

class AddressResponse(AddressRead):
    pass

class AddressDetails(BaseModel):
    google_place_id: Optional[str] = None
    formatted_address: Optional[str] = None
    street_number: Optional[str] = None
    street_name: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


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
    job_number: Optional[str] = None

class BookingCreate(BaseModel):
    pickupAddress: Optional[str] = None
    pickup_address_details: Optional[str] = None  # JSON string
    pickup_date: date
    pickup_time: Optional[time] = None
    dropoffAddress: Optional[str] = None
    dropoff_address_details: Optional[str] = None  # JSON string
    dropoff_date: date
    dropoff_time: Optional[time] = None
    notes: Optional[str] = None
    job_number: Optional[str] = None
    creator_id: Optional[int] = 1

class BookingUpdate(BaseModel):
    completion: Optional[bool] = None
    pickup_complete: Optional[datetime] = None
    dropoff_complete: Optional[datetime] = None

class BookingRead(BookingBase):
    booking_id: int
    attachments: Optional[int] = None
    pickup_complete: Optional[datetime] = None
    dropoff_complete: Optional[datetime] = None
    created: Optional[datetime] = None
    completion: bool = False
    
    class Config:
        from_attributes = True

class BookingResponse(BookingRead):
    pickup_address: Optional[AddressResponse] = None
    dropoff_address: Optional[AddressResponse] = None


# Attachment Schemas
class AttachmentBase(BaseModel):
    booking_id: Optional[int] = None
    dropbox_path: Optional[str] = None
    dropbox_shared_url: Optional[str] = None
    uploaded_by: Optional[int] = None

class AttachmentCreate(AttachmentBase):
    pass

class AttachmentRead(AttachmentBase):
    attachment_id: int
    uploaded_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AttachmentResponse(AttachmentRead):
    pass


# ============================================================================
# ADDITIONAL REQUEST/RESPONSE SCHEMAS
# ============================================================================

# Job Status Update Schemas
class JobStatusUpdate(BaseModel):
    job_status_id: int

class JobAddressUpdate(BaseModel):
    job_address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None

class JobBillingUpdate(BaseModel):
    billing_entity: Optional[int] = None

class ApproveQuoteRequest(BaseModel):
    approved_quote: Optional[int] = None


# Variable Option Costs
class VariableOptionCostsRequest(BaseModel):
    option_ids: List[int]

class VariableOptionCostResponse(BaseModel):
    variable_option_id: int
    base_cost: float
    multiplier_cost: float


# Update forward references for nested models
ClientResponse.model_rebuild()
ProductResponse.model_rebuild()
QuoteDetailResponse.model_rebuild()
