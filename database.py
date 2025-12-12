from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
# Import all models to ensure they're registered with Base
from models import (
    Client, Contact, Billing,
    ProductCategory, Product, ProductVariable, VariableOption, ProductProductVariable, MeasureType,
    Project, Quote, Job, Item, ItemVariable, ItemVariableOption,
    JobStatus, JobStatusHistory,
    Staff,
    ThroughputStatus, ThroughputStage, ThroughputTask, ThroughputStageDate,
    Address, Booking, Attachment
)
from config import DATABASE_URL, DB_ECHO, DB_POOL_SIZE, DB_MAX_OVERFLOW, DB_POOL_RECYCLE

# Create engine with configuration from config.py
engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_recycle=DB_POOL_RECYCLE
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize the database with tables"""
    create_tables()
    print("Database initialized successfully!")

