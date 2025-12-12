"""
Job domain models including projects, quotes, items, workflow, and delivery
"""
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, Text, Boolean, Date, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, date
from . import Base


class Project(Base):
    """Project schema for storing project information"""
    __tablename__ = 'projects'
    __table_args__ = {'schema': 'job'}
    
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    address = Column(Text)
    suburb = Column(Text)
    state = Column(Text)  # Enum_Common.State equivalent
    postcode = Column(Integer)  # Numeric(4) equivalent
    date_created = Column(Date, default=datetime.utcnow().date())
    
    # Relationships
    jobs = relationship("Job", back_populates="project")
    
    def __repr__(self):
        return f"<Project(project_id={self.project_id}, name='{self.name}')>"


class JobStatus(Base):
    """Job Status schema for storing available job statuses"""
    __tablename__ = 'job_statuses'
    __table_args__ = {'schema': 'job'}
    
    job_status_id = Column(Integer, primary_key=True, autoincrement=True)
    job_status = Column(Text, nullable=False)
    
    # Relationships
    status_history = relationship("JobStatusHistory", back_populates="job_status")
    
    def __repr__(self):
        return f"<JobStatus(job_status_id={self.job_status_id}, job_status='{self.job_status}')>"


class Job(Base):
    """Job schema for storing job information"""
    __tablename__ = 'jobs'
    __table_args__ = {'schema': 'job'}
    
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    reference = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey('job.projects.project_id'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.clients.client_id'), nullable=False)
    billing_entity = Column(Integer, ForeignKey('client.billing.billing_id'), nullable=True)
    po = Column(Text)  # Purchase Order
    date_created = Column(Date, default=datetime.utcnow().date())
    contact_id = Column(Integer, ForeignKey('client.contacts.contact_id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.staff.staff_id'), nullable=False)
    job_status_id = Column(Integer, ForeignKey('job.job_statuses.job_status_id'))
    job_address = Column(Text)
    suburb = Column(Text)
    state = Column(Text)
    postcode = Column(Integer)
    approved_quote = Column(Integer, ForeignKey('job.quote.quote_id'), nullable=True)
    stage_id = Column(Integer, ForeignKey('throughput.stage.stage_id'), nullable=True)
    assets = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="jobs")
    client = relationship("Client", back_populates="jobs")
    billing = relationship("Billing")
    contact = relationship("Contact", back_populates="jobs")
    staff = relationship("Staff", back_populates="assigned_jobs")
    job_status = relationship("JobStatus")
    status_history = relationship("JobStatusHistory", back_populates="job", cascade="all, delete-orphan")
    approved_quote_rel = relationship("Quote", foreign_keys=[approved_quote])
    stage = relationship("ThroughputStage")
    
    def __repr__(self):
        return f"<Job(job_id={self.job_id}, reference='{self.reference}')>"


class JobStatusHistory(Base):
    """Job Status History schema for tracking job status changes"""
    __tablename__ = 'job_status_history'
    __table_args__ = {'schema': 'job'}
    
    job_status_history_id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('job.jobs.job_id'), nullable=False)
    job_status_id = Column(Integer, ForeignKey('job.job_statuses.job_status_id'), nullable=False)
    date = Column(Date, default=datetime.utcnow().date())
    
    # Relationships
    job = relationship("Job", back_populates="status_history")
    job_status = relationship("JobStatus", back_populates="status_history")
    
    def __repr__(self):
        return f"<JobStatusHistory(job_status_history_id={self.job_status_history_id}, job_id={self.job_id})>"


class Quote(Base):
    """Quote schema for storing quote information"""
    __tablename__ = 'quote'
    __table_args__ = {'schema': 'job'}
    
    quote_id = Column(Integer, primary_key=True, autoincrement=True)
    quote_number = Column(Text, nullable=False)  # Format: job_id-quote_number (e.g., "156-001")
    job_id = Column(Integer, ForeignKey('job.jobs.job_id'), nullable=False)
    date_created = Column(Date, default=datetime.utcnow().date())
    cost_excl_gst = Column(Float)
    cost_incl_gst = Column(Float)
    
    # Relationships
    job = relationship("Job", foreign_keys=[job_id])
    items = relationship("Item", back_populates="quote", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Quote(quote_id={self.quote_id}, quote_number='{self.quote_number}', job_id={self.job_id})>"


class Item(Base):
    """Item schema for storing quote items"""
    __tablename__ = 'items'
    __table_args__ = {'schema': 'job'}
    
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    quote_id = Column(Integer, ForeignKey('job.quote.quote_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.products.product_id'), nullable=False)
    reference = Column(Text, nullable=False, default='')
    notes = Column(Text)
    quantity = Column(Float, nullable=False)
    length = Column(Numeric)
    height = Column(Numeric)
    cost_excl_gst = Column(Float)
    cost_incl_gst = Column(Float)
    
    # Relationships
    quote = relationship("Quote", back_populates="items")
    product = relationship("Product", back_populates="items")
    item_variables = relationship("ItemVariable", back_populates="item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Item(item_id={self.item_id}, quote_id={self.quote_id}, product_id={self.product_id})>"


class ItemVariable(Base):
    """Item Variable schema for storing item-specific variable selections"""
    __tablename__ = 'item_variables'
    __table_args__ = {'schema': 'job'}
    
    item_variable_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('job.items.item_id'), nullable=False)
    product_variable_id = Column(Integer, ForeignKey('product.product_variables.product_variable_id'), nullable=False)
    
    # Relationships
    item = relationship("Item", back_populates="item_variables")
    product_variable = relationship("ProductVariable", back_populates="item_variables")
    item_variable_options = relationship("ItemVariableOption", back_populates="item_variable", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ItemVariable(item_variable_id={self.item_variable_id}, item_id={self.item_id})>"


class ItemVariableOption(Base):
    """Item Variable Option schema for storing selected options for item variables"""
    __tablename__ = 'item_variable_options'
    __table_args__ = {'schema': 'job'}
    
    item_variable_option_id = Column(Integer, primary_key=True, autoincrement=True)
    item_variable_id = Column(Integer, ForeignKey('job.item_variables.item_variable_id'), nullable=False)
    variable_option_id = Column(Integer, ForeignKey('product.variable_options.variable_option_id'), nullable=False)
    
    # Relationships
    item_variable = relationship("ItemVariable", back_populates="item_variable_options")
    variable_option = relationship("VariableOption", back_populates="item_variable_options")
    
    def __repr__(self):
        return f"<ItemVariableOption(item_variable_option_id={self.item_variable_option_id}, item_variable_id={self.item_variable_id})>"



