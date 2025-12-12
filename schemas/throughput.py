"""
Pydantic schemas for Throughput domain models
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


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


# ThroughputTask Schemas
class ThroughputTaskBase(BaseModel):
    task_name: str
    job_number: int
    item_id: Optional[int] = None
    stage_id: int
    status_id: int
    task_order: int
    time_completed: Optional[datetime] = None


class ThroughputTaskCreate(ThroughputTaskBase):
    pass


class ThroughputTaskRead(ThroughputTaskBase):
    task_id: int
    
    class Config:
        from_attributes = True


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

