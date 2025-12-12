"""
Pydantic schemas package for FastAPI request/response validation
Organized by domain to match models/ folder structure
"""
from typing import Optional, List
from datetime import date, datetime, time

# Import all schemas
from .client import (
    ClientBase, ClientCreate, ClientRead,
    ContactBase, ContactCreate, ContactRead,
    BillingBase, BillingCreate, BillingRead
)
from .product import (
    ProductCategoryBase, ProductCategoryCreate, ProductCategoryRead,
    MeasureTypeBase, MeasureTypeCreate, MeasureTypeRead,
    ProductBase, ProductCreate, ProductRead,
    ProductVariableBase, ProductVariableCreate, ProductVariableRead,
    VariableOptionBase, VariableOptionCreate, VariableOptionRead,
    ProductProductVariableBase, ProductProductVariableCreate, ProductProductVariableRead
)
from .staff import (
    StaffBase, StaffCreate, StaffRead
)
from .job import (
    ProjectBase, ProjectCreate, ProjectRead,
    JobStatusBase, JobStatusCreate, JobStatusRead,
    JobBase, JobCreate, JobRead,
    JobStatusHistoryBase, JobStatusHistoryCreate, JobStatusHistoryRead,
    QuoteBase, QuoteCreate, QuoteRead,
    ItemBase, ItemCreate, ItemRead,
    ItemVariableBase, ItemVariableCreate, ItemVariableRead,
    ItemVariableOptionBase, ItemVariableOptionCreate, ItemVariableOptionRead
)
from .delivery import (
    AddressBase, AddressCreate, AddressRead,
    BookingBase, BookingCreate, BookingRead,
    AttachmentBase, AttachmentCreate, AttachmentRead
)
from .throughput import (
    ThroughputStatusBase, ThroughputStatusCreate, ThroughputStatusRead,
    ThroughputStageBase, ThroughputStageCreate, ThroughputStageRead,
    ThroughputTaskBase, ThroughputTaskCreate, ThroughputTaskRead,
    ThroughputStageDateBase, ThroughputStageDateCreate, ThroughputStageDateRead
)
# Public schema imports - add when models exist
# from .public import (...)

__all__ = [
    # Client schemas
    "ClientBase", "ClientCreate", "ClientRead",
    "ContactBase", "ContactCreate", "ContactRead",
    "BillingBase", "BillingCreate", "BillingRead",
    # Product schemas
    "ProductCategoryBase", "ProductCategoryCreate", "ProductCategoryRead",
    "MeasureTypeBase", "MeasureTypeCreate", "MeasureTypeRead",
    "ProductBase", "ProductCreate", "ProductRead",
    "ProductVariableBase", "ProductVariableCreate", "ProductVariableRead",
    "VariableOptionBase", "VariableOptionCreate", "VariableOptionRead",
    "ProductProductVariableBase", "ProductProductVariableCreate", "ProductProductVariableRead",
    # Staff schemas
    "StaffBase", "StaffCreate", "StaffRead",
    # Job schemas
    "ProjectBase", "ProjectCreate", "ProjectRead",
    "JobStatusBase", "JobStatusCreate", "JobStatusRead",
    "JobBase", "JobCreate", "JobRead",
    "JobStatusHistoryBase", "JobStatusHistoryCreate", "JobStatusHistoryRead",
    "QuoteBase", "QuoteCreate", "QuoteRead",
    "ItemBase", "ItemCreate", "ItemRead",
    "ItemVariableBase", "ItemVariableCreate", "ItemVariableRead",
    "ItemVariableOptionBase", "ItemVariableOptionCreate", "ItemVariableOptionRead",
    # Delivery schemas
    "AddressBase", "AddressCreate", "AddressRead",
    "BookingBase", "BookingCreate", "BookingRead",
    "AttachmentBase", "AttachmentCreate", "AttachmentRead",
    # Throughput schemas
    "ThroughputStatusBase", "ThroughputStatusCreate", "ThroughputStatusRead",
    "ThroughputStageBase", "ThroughputStageCreate", "ThroughputStageRead",
    "ThroughputTaskBase", "ThroughputTaskCreate", "ThroughputTaskRead",
    "ThroughputStageDateBase", "ThroughputStageDateCreate", "ThroughputStageDateRead",
]

