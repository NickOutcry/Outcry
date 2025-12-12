"""
Throughput domain models - Workflow and task tracking
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base


class ThroughputStatus(Base):
    """Status schema for throughput tracking"""
    __tablename__ = 'status'
    __table_args__ = {'schema': 'throughput'}
    
    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Text, nullable=False)
    
    # Relationships
    tasks = relationship("ThroughputTask", back_populates="status")
    
    def __repr__(self):
        return f"<ThroughputStatus(status_id={self.status_id}, status='{self.status}')>"


class ThroughputStage(Base):
    """Stage schema for throughput tracking"""
    __tablename__ = 'stage'
    __table_args__ = {'schema': 'throughput'}
    
    stage_id = Column(Integer, primary_key=True, autoincrement=True)
    stage = Column(Text, nullable=False)
    stage_order = Column(Integer, nullable=False)
    
    # Relationships
    tasks = relationship("ThroughputTask", back_populates="stage")
    stage_dates = relationship("ThroughputStageDate", back_populates="stage")
    
    def __repr__(self):
        return f"<ThroughputStage(stage_id={self.stage_id}, stage='{self.stage}', stage_order={self.stage_order})>"


class ThroughputTask(Base):
    """Task schema for throughput tracking"""
    __tablename__ = 'task'
    __table_args__ = {'schema': 'throughput'}
    
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(Text, nullable=False)
    job_number = Column(Integer, ForeignKey('job.jobs.job_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('job.items.item_id'), nullable=True)
    stage_id = Column(Integer, ForeignKey('throughput.stage.stage_id'), nullable=False)
    status_id = Column(Integer, ForeignKey('throughput.status.status_id'), nullable=False)
    task_order = Column(Integer, nullable=False)
    time_completed = Column(DateTime, nullable=True)
    
    # Relationships
    job = relationship("Job")
    item = relationship("Item")
    stage = relationship("ThroughputStage", back_populates="tasks")
    status = relationship("ThroughputStatus", back_populates="tasks")
    
    def __repr__(self):
        return f"<ThroughputTask(task_id={self.task_id}, task_name='{self.task_name}', job_number={self.job_number})>"


class ThroughputStageDate(Base):
    """Stage Dates schema for tracking due dates for job stages"""
    __tablename__ = 'stage_dates'
    __table_args__ = {'schema': 'throughput'}
    
    stage_date_id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('job.jobs.job_id'), nullable=False)
    status_id = Column(Integer, ForeignKey('throughput.stage.stage_id'), nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Relationships
    job = relationship("Job")
    stage = relationship("ThroughputStage", back_populates="stage_dates")
    
    def __repr__(self):
        return f"<ThroughputStageDate(stage_date_id={self.stage_date_id}, job_id={self.job_id}, status_id={self.status_id}, due_date='{self.due_date}')>"

