"""
Public schema router
General/system tables that don't belong to specific domains

Note: Add routes here when public schema models are created
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text

from database import SessionLocal
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["public"])


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Placeholder for future public schema routes
# When models are added to models/public.py, create corresponding routes here
# following the same CRUD pattern as other routers

# Example structure:
# @router.get("/your-table", response_model=List[YourTableRead])
# async def get_your_tables(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db)
# ):
#     """Get all your_table records"""
#     records = db.query(YourTable).offset(skip).limit(limit).all()
#     return records
#
# @router.get("/your-table/{id}", response_model=YourTableRead)
# async def get_your_table(id: int, db: Session = Depends(get_db)):
#     """Get a single your_table record by ID"""
#     record = db.query(YourTable).filter(YourTable.id == id).first()
#     if not record:
#         raise HTTPException(status_code=404, detail="Record not found")
#     return record
#
# @router.post("/your-table", response_model=YourTableRead, status_code=201)
# async def create_your_table(record: YourTableCreate, db: Session = Depends(get_db)):
#     """Create a new your_table record"""
#     db_record = YourTable(**record.model_dump())
#     db.add(db_record)
#     db.commit()
#     db.refresh(db_record)
#     return db_record
#
# @router.put("/your-table/{id}", response_model=YourTableRead)
# async def update_your_table(
#     id: int,
#     record: YourTableBase,
#     db: Session = Depends(get_db)
# ):
#     """Update an existing your_table record"""
#     db_record = db.query(YourTable).filter(YourTable.id == id).first()
#     if not db_record:
#         raise HTTPException(status_code=404, detail="Record not found")
#     
#     for key, value in record.model_dump(exclude_unset=True).items():
#         setattr(db_record, key, value)
#     
#     db.commit()
#     db.refresh(db_record)
#     return db_record
#
# @router.delete("/your-table/{id}", status_code=204)
# async def delete_your_table(id: int, db: Session = Depends(get_db)):
#     """Delete a your_table record"""
#     db_record = db.query(YourTable).filter(YourTable.id == id).first()
#     if not db_record:
#         raise HTTPException(status_code=404, detail="Record not found")
#     
#     db.delete(db_record)
#     db.commit()
#     return None


# ============================================================================
# TEST ENDPOINT
# ============================================================================

@router.get("/public/test", response_class=JSONResponse)
async def test_public_connection(db: Session = Depends(get_db)):
    """
    Test endpoint to verify database connection.
    Public schema currently has no models, so this just tests the connection.
    """
    try:
        # Test database connection by executing a simple query
        db.execute(text("SELECT 1"))
        return {
            "status": "success",
            "message": "Database connection is working",
            "data": {
                "note": "Public schema has no models defined yet"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}",
            "data": None
        }

