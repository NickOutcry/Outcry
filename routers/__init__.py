"""
FastAPI routers for each domain
"""
from .client import router as client_router
from .product import router as product_router
from .job import router as job_router
from .staff import router as staff_router
from .upload import router as upload_router
from .delivery import router as delivery_router
from .throughput import router as throughput_router
from .public import router as public_router

__all__ = [
    "client_router",
    "product_router",
    "job_router",
    "staff_router",
    "upload_router",
    "delivery_router",
    "throughput_router",
    "public_router",
]

