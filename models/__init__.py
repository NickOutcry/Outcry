"""
Models package for Outcry Projects
All SQLAlchemy models are organized by domain
"""
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

# Import all models to ensure they're registered with Base
from .client import Client, Contact, Billing
from .product import ProductCategory, Product, ProductVariable, VariableOption, ProductProductVariable, MeasureType
from .job import (
    Project, Quote, Job, Item, ItemVariable, ItemVariableOption,
    JobStatus, JobStatusHistory
)
from .staff import Staff
from .throughput import ThroughputStatus, ThroughputStage, ThroughputTask, ThroughputStageDate
from .delivery import Address, Booking, Attachment
from .public import *  # Import any public schema models

# Export all models
__all__ = [
    "Base",
    # Client models
    "Client",
    "Contact",
    "Billing",
    # Product models
    "ProductCategory",
    "Product",
    "ProductVariable",
    "VariableOption",
    "ProductProductVariable",
    "MeasureType",
    # Job models
    "Project",
    "Quote",
    "Job",
    "Item",
    "ItemVariable",
    "ItemVariableOption",
    "JobStatus",
    "JobStatusHistory",
    # Staff models
    "Staff",
    # Throughput models
    "ThroughputStatus",
    "ThroughputStage",
    "ThroughputTask",
    "ThroughputStageDate",
    # Delivery models
    "Address",
    "Booking",
    "Attachment",
]

