"""
Throughput domain router - ThroughputStatus, ThroughputStage, ThroughputTask, ThroughputStageDate CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

from database import SessionLocal
from models.throughput import ThroughputStatus, ThroughputStage, ThroughputTask, ThroughputStageDate
from schemas.throughput import (
    ThroughputStatusBase, ThroughputStatusCreate, ThroughputStatusRead,
    ThroughputStageBase, ThroughputStageCreate, ThroughputStageRead,
    ThroughputTaskBase, ThroughputTaskCreate, ThroughputTaskRead,
    ThroughputStageDateBase, ThroughputStageDateCreate, ThroughputStageDateRead
)
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["throughput"])


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# THROUGHPUT STATUS ROUTES
# ============================================================================

@router.get("/throughput/statuses", response_model=List[ThroughputStatusRead])
async def get_throughput_statuses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all throughput statuses"""
    statuses = db.query(ThroughputStatus).offset(skip).limit(limit).all()
    return statuses


@router.get("/throughput/statuses/{status_id}", response_model=ThroughputStatusRead)
async def get_throughput_status(status_id: int, db: Session = Depends(get_db)):
    """Get a single throughput status by ID"""
    status = db.query(ThroughputStatus).filter(ThroughputStatus.status_id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Throughput status not found")
    return status


@router.post("/throughput/statuses", response_model=ThroughputStatusRead, status_code=201)
async def create_throughput_status(
    status: ThroughputStatusCreate,
    db: Session = Depends(get_db)
):
    """Create a new throughput status"""
    db_status = ThroughputStatus(**status.model_dump())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


@router.put("/throughput/statuses/{status_id}", response_model=ThroughputStatusRead)
async def update_throughput_status(
    status_id: int,
    status: ThroughputStatusBase,
    db: Session = Depends(get_db)
):
    """Update an existing throughput status"""
    db_status = db.query(ThroughputStatus).filter(ThroughputStatus.status_id == status_id).first()
    if not db_status:
        raise HTTPException(status_code=404, detail="Throughput status not found")
    
    for key, value in status.model_dump(exclude_unset=True).items():
        setattr(db_status, key, value)
    
    db.commit()
    db.refresh(db_status)
    return db_status


@router.delete("/throughput/statuses/{status_id}", status_code=204)
async def delete_throughput_status(status_id: int, db: Session = Depends(get_db)):
    """Delete a throughput status"""
    db_status = db.query(ThroughputStatus).filter(ThroughputStatus.status_id == status_id).first()
    if not db_status:
        raise HTTPException(status_code=404, detail="Throughput status not found")
    
    db.delete(db_status)
    db.commit()
    return None


# ============================================================================
# THROUGHPUT STAGE ROUTES
# ============================================================================

@router.get("/throughput/stages", response_model=List[ThroughputStageRead])
async def get_throughput_stages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all throughput stages"""
    stages = db.query(ThroughputStage).offset(skip).limit(limit).all()
    return stages


@router.get("/throughput/stages/{stage_id}", response_model=ThroughputStageRead)
async def get_throughput_stage(stage_id: int, db: Session = Depends(get_db)):
    """Get a single throughput stage by ID"""
    stage = db.query(ThroughputStage).filter(ThroughputStage.stage_id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Throughput stage not found")
    return stage


@router.post("/throughput/stages", response_model=ThroughputStageRead, status_code=201)
async def create_throughput_stage(
    stage: ThroughputStageCreate,
    db: Session = Depends(get_db)
):
    """Create a new throughput stage"""
    db_stage = ThroughputStage(**stage.model_dump())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage


@router.put("/throughput/stages/{stage_id}", response_model=ThroughputStageRead)
async def update_throughput_stage(
    stage_id: int,
    stage: ThroughputStageBase,
    db: Session = Depends(get_db)
):
    """Update an existing throughput stage"""
    db_stage = db.query(ThroughputStage).filter(ThroughputStage.stage_id == stage_id).first()
    if not db_stage:
        raise HTTPException(status_code=404, detail="Throughput stage not found")
    
    for key, value in stage.model_dump(exclude_unset=True).items():
        setattr(db_stage, key, value)
    
    db.commit()
    db.refresh(db_stage)
    return db_stage


@router.delete("/throughput/stages/{stage_id}", status_code=204)
async def delete_throughput_stage(stage_id: int, db: Session = Depends(get_db)):
    """Delete a throughput stage"""
    db_stage = db.query(ThroughputStage).filter(ThroughputStage.stage_id == stage_id).first()
    if not db_stage:
        raise HTTPException(status_code=404, detail="Throughput stage not found")
    
    db.delete(db_stage)
    db.commit()
    return None


# ============================================================================
# THROUGHPUT TASK ROUTES
# ============================================================================

@router.get("/throughput/tasks", response_model=List[ThroughputTaskRead])
async def get_throughput_tasks(
    skip: int = 0,
    limit: int = 100,
    job_number: Optional[int] = None,
    stage_id: Optional[int] = None,
    status_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all throughput tasks, optionally filtered by job_number, stage_id, or status_id"""
    query = db.query(ThroughputTask)
    if job_number is not None:
        query = query.filter(ThroughputTask.job_number == job_number)
    if stage_id is not None:
        query = query.filter(ThroughputTask.stage_id == stage_id)
    if status_id is not None:
        query = query.filter(ThroughputTask.status_id == status_id)
    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get("/throughput/tasks/{task_id}", response_model=ThroughputTaskRead)
async def get_throughput_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single throughput task by ID"""
    task = db.query(ThroughputTask).filter(ThroughputTask.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Throughput task not found")
    return task


@router.post("/throughput/tasks", response_model=ThroughputTaskRead, status_code=201)
async def create_throughput_task(
    task: ThroughputTaskCreate,
    db: Session = Depends(get_db)
):
    """Create a new throughput task"""
    db_task = ThroughputTask(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/throughput/tasks/{task_id}", response_model=ThroughputTaskRead)
async def update_throughput_task(
    task_id: int,
    task: ThroughputTaskBase,
    db: Session = Depends(get_db)
):
    """Update an existing throughput task"""
    db_task = db.query(ThroughputTask).filter(ThroughputTask.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Throughput task not found")
    
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/throughput/tasks/{task_id}", status_code=204)
async def delete_throughput_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a throughput task"""
    db_task = db.query(ThroughputTask).filter(ThroughputTask.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Throughput task not found")
    
    db.delete(db_task)
    db.commit()
    return None


# ============================================================================
# THROUGHPUT STAGE DATE ROUTES
# ============================================================================

@router.get("/throughput/stage-dates", response_model=List[ThroughputStageDateRead])
async def get_throughput_stage_dates(
    skip: int = 0,
    limit: int = 100,
    job_id: Optional[int] = None,
    status_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all throughput stage dates, optionally filtered by job_id or status_id"""
    query = db.query(ThroughputStageDate)
    if job_id is not None:
        query = query.filter(ThroughputStageDate.job_id == job_id)
    if status_id is not None:
        query = query.filter(ThroughputStageDate.status_id == status_id)
    stage_dates = query.offset(skip).limit(limit).all()
    return stage_dates


@router.get("/throughput/stage-dates/{stage_date_id}", response_model=ThroughputStageDateRead)
async def get_throughput_stage_date(stage_date_id: int, db: Session = Depends(get_db)):
    """Get a single throughput stage date by ID"""
    stage_date = db.query(ThroughputStageDate).filter(
        ThroughputStageDate.stage_date_id == stage_date_id
    ).first()
    if not stage_date:
        raise HTTPException(status_code=404, detail="Throughput stage date not found")
    return stage_date


@router.post("/throughput/stage-dates", response_model=ThroughputStageDateRead, status_code=201)
async def create_throughput_stage_date(
    stage_date: ThroughputStageDateCreate,
    db: Session = Depends(get_db)
):
    """Create a new throughput stage date"""
    db_stage_date = ThroughputStageDate(**stage_date.model_dump())
    db.add(db_stage_date)
    db.commit()
    db.refresh(db_stage_date)
    return db_stage_date


@router.put("/throughput/stage-dates/{stage_date_id}", response_model=ThroughputStageDateRead)
async def update_throughput_stage_date(
    stage_date_id: int,
    stage_date: ThroughputStageDateBase,
    db: Session = Depends(get_db)
):
    """Update an existing throughput stage date"""
    db_stage_date = db.query(ThroughputStageDate).filter(
        ThroughputStageDate.stage_date_id == stage_date_id
    ).first()
    if not db_stage_date:
        raise HTTPException(status_code=404, detail="Throughput stage date not found")
    
    for key, value in stage_date.model_dump(exclude_unset=True).items():
        setattr(db_stage_date, key, value)
    
    db.commit()
    db.refresh(db_stage_date)
    return db_stage_date


@router.delete("/throughput/stage-dates/{stage_date_id}", status_code=204)
async def delete_throughput_stage_date(stage_date_id: int, db: Session = Depends(get_db)):
    """Delete a throughput stage date"""
    db_stage_date = db.query(ThroughputStageDate).filter(
        ThroughputStageDate.stage_date_id == stage_date_id
    ).first()
    if not db_stage_date:
        raise HTTPException(status_code=404, detail="Throughput stage date not found")
    
    db.delete(db_stage_date)
    db.commit()
    return None


# ============================================================================
# TEST ENDPOINT
# ============================================================================

@router.get("/throughput/test", response_class=JSONResponse)
async def test_throughput_connection(db: Session = Depends(get_db)):
    """
    Test endpoint to verify database connection and models.
    Returns the first record from ThroughputStatus, ThroughputStage, ThroughputTask, and ThroughputStageDate tables.
    """
    result = {
        "status": "success",
        "message": "Database connection and models are working",
        "data": {}
    }
    
    try:
        # Test ThroughputStatus table
        first_status = db.query(ThroughputStatus).first()
        if first_status:
            result["data"]["status"] = {
                "status_id": first_status.status_id,
                "status": first_status.status
            }
        else:
            result["data"]["status"] = None
        
        # Test ThroughputStage table
        first_stage = db.query(ThroughputStage).first()
        if first_stage:
            result["data"]["stage"] = {
                "stage_id": first_stage.stage_id,
                "stage": first_stage.stage,
                "stage_order": first_stage.stage_order
            }
        else:
            result["data"]["stage"] = None
        
        # Test ThroughputTask table
        first_task = db.query(ThroughputTask).first()
        if first_task:
            result["data"]["task"] = {
                "task_id": first_task.task_id,
                "task_name": first_task.task_name,
                "job_number": first_task.job_number,
                "stage_id": first_task.stage_id,
                "status_id": first_task.status_id
            }
        else:
            result["data"]["task"] = None
        
        # Test ThroughputStageDate table
        first_stage_date = db.query(ThroughputStageDate).first()
        if first_stage_date:
            result["data"]["stage_date"] = {
                "stage_date_id": first_stage_date.stage_date_id,
                "job_id": first_stage_date.job_id,
                "status_id": first_stage_date.status_id,
                "due_date": first_stage_date.due_date.isoformat() if first_stage_date.due_date else None
            }
        else:
            result["data"]["stage_date"] = None
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}",
            "data": {}
        }

