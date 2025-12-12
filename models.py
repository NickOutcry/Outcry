from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean, Date, Numeric, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Client(Base):
    """Client schema for storing client information"""
    __tablename__ = 'clients'
    __table_args__ = {'schema': 'client'}
    
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    address = Column(Text)
    suburb = Column(Text)
    state = Column(Text)
    postcode = Column(Integer)  # Numeric(4) equivalent
    
    # Relationships
    contacts = relationship("Contact", back_populates="client")
    billing = relationship("Billing", back_populates="client")
    jobs = relationship("Job", back_populates="client")
    
    def __repr__(self):
        return f"<Client(client_id={self.client_id}, name='{self.name}')>"

class Contact(Base):
    """Contact schema for storing client contact information"""
    __tablename__ = 'contacts'
    __table_args__ = {'schema': 'client'}
    
    contact_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    email = Column(Text)
    phone = Column(Text)
    client_id = Column(Integer, ForeignKey('client.clients.client_id'), nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="contacts")
    jobs = relationship("Job", back_populates="contact")
    
    def __repr__(self):
        return f"<Contact(contact_id={self.contact_id}, name='{self.first_name} {self.surname}')>"

class Billing(Base):
    """Billing schema for storing client billing information"""
    __tablename__ = 'billing'
    __table_args__ = {'schema': 'client'}
    
    billing_id = Column(Integer, primary_key=True, autoincrement=True)
    entity = Column(Text, nullable=False)
    address = Column(Text)
    suburb = Column(Text)
    state = Column(Text)
    postcode = Column(Integer)  # Numeric(4) equivalent
    client_id = Column(Integer, ForeignKey('client.clients.client_id'), nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="billing")
    
    def __repr__(self):
        return f"<Billing(billing_id={self.billing_id}, entity='{self.entity}')>"

class ProductCategory(Base):
    """Product Category schema for categorizing products"""
    __tablename__ = 'product_categories'
    __table_args__ = {'schema': 'product'}
    
    product_category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    
    # Relationships
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<ProductCategory(product_category_id={self.product_category_id}, name='{self.name}')>"

class Product(Base):
    """Product schema for storing product information"""
    __tablename__ = 'products'
    __table_args__ = {'schema': 'product'}
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    product_category_id = Column(Integer, ForeignKey('product.product_categories.product_category_id'), nullable=False)
    measure_type_id = Column(Integer, ForeignKey('product.measure_type.measure_type_id'), nullable=True)
    
    # Relationships
    category = relationship("ProductCategory", back_populates="products")
    measure_type = relationship("MeasureType")
    product_variable_assignments = relationship(
        "ProductProductVariable",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    variables = relationship(
        "ProductVariable",
        secondary="product.product_product_variable",
        back_populates="products",
        order_by="ProductProductVariable.display_order"
    )
    items = relationship("Item", back_populates="product")
    
    def __repr__(self):
        return f"<Product(product_id={self.product_id}, name='{self.name}')>"

class ProductVariable(Base):
    """Product Variable schema for storing product variations"""
    __tablename__ = 'product_variables'
    __table_args__ = {'schema': 'product'}
    
    product_variable_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    data_type = Column(Text, nullable=False)
    
    # Relationships
    options = relationship("VariableOption", back_populates="product_variable")
    item_variables = relationship("ItemVariable", back_populates="product_variable")
    product_assignments = relationship(
        "ProductProductVariable",
        back_populates="product_variable",
        cascade="all, delete-orphan"
    )
    products = relationship(
        "Product",
        secondary="product.product_product_variable",
        back_populates="variables"
    )
    
    def __repr__(self):
        return f"<ProductVariable(product_variable_id={self.product_variable_id}, name='{self.name}')>"

class VariableOption(Base):
    """Variable Option schema for storing specific options of product variables"""
    __tablename__ = 'variable_options'
    __table_args__ = {'schema': 'product'}
    
    variable_option_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    base_cost = Column(Float, nullable=False)
    multiplier_cost = Column(Float, nullable=False)
    product_variable_id = Column(Integer, ForeignKey('product.product_variables.product_variable_id'), nullable=False)
    
    # Relationships
    product_variable = relationship("ProductVariable", back_populates="options")
    item_variable_options = relationship("ItemVariableOption", back_populates="variable_option")
    
    def __repr__(self):
        return f"<VariableOption(variable_option_id={self.variable_option_id}, name='{self.name}')>"


class ProductProductVariable(Base):
    """Join table to control which variables are assigned to a product and their order"""
    __tablename__ = 'product_product_variable'
    __table_args__ = {'schema': 'product'}

    product_product_variable = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.products.product_id', ondelete='CASCADE'), nullable=False)
    product_variable_id = Column(Integer, ForeignKey('product.product_variables.product_variable_id', ondelete='CASCADE'), nullable=False)
    display_order = Column(Integer)

    # Relationships
    product = relationship("Product", back_populates="product_variable_assignments")
    product_variable = relationship("ProductVariable", back_populates="product_assignments")

    def __repr__(self):
        return (
            f"<ProductProductVariable("
            f"product_product_variable={self.product_product_variable}, "
            f"product_id={self.product_id}, "
            f"product_variable_id={self.product_variable_id}, "
            f"display_order={self.display_order}"
            f")>"
        )

class MeasureType(Base):
    """Measure Type schema for storing measurement types"""
    __tablename__ = 'measure_type'
    __table_args__ = {'schema': 'product'}
    
    measure_type_id = Column(Integer, primary_key=True, autoincrement=True)
    measure_type = Column(Text, nullable=False)
    
    # Relationships
    products = relationship("Product", back_populates="measure_type")
    
    def __repr__(self):
        return f"<MeasureType(measure_type_id={self.measure_type_id}, measure_type='{self.measure_type}')>"

class Staff(Base):
    """Staff schema for storing employee information"""
    __tablename__ = 'staff'
    __table_args__ = {'schema': 'staff'}
    
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text)
    address = Column(Text)
    suburb = Column(Text)
    state = Column(Text)  # Enum_Common.State equivalent
    postcode = Column(Integer)  # Numeric(4) equivalent
    dob = Column(Date)  # Date of Birth
    emergency_contact = Column(Text)
    emergency_contact_number = Column(Text)
    email = Column(Text)
    
    # Relationships
    assigned_jobs = relationship("Job", back_populates="staff")
    
    def __repr__(self):
        return f"<Staff(staff_id={self.staff_id}, name='{self.first_name} {self.surname}')>"

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

# Throughput Schema Models
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
    stage = relationship("ThroughputStage")
    
    def __repr__(self):
        return f"<ThroughputStageDate(stage_date_id={self.stage_date_id}, job_id={self.job_id}, status_id={self.status_id}, due_date='{self.due_date}')>"


# Delivery Schema Models
class Address(Base):
    """Address schema for storing address information"""
    __tablename__ = 'address'
    __table_args__ = {'schema': 'delivery'}
    
    address_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    google_place_id = Column(String(255))
    formatted_address = Column(Text)
    street_number = Column(String(50))
    street_name = Column(String(255))
    suburb = Column(String(100))
    state = Column(String(50))
    postcode = Column(String(10))
    country = Column(String(100))
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    
    def __repr__(self):
        return f"<Address(address_id={self.address_id}, formatted_address='{self.formatted_address}')>"


class Booking(Base):
    """Booking schema for storing delivery booking information"""
    __tablename__ = 'booking'
    __table_args__ = {'schema': 'delivery'}
    
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    pickup_address_id = Column(Integer, ForeignKey('delivery.address.address_id'))
    pickup_date = Column(Date, nullable=False)
    pickup_time = Column(Time)
    dropoff_address_id = Column(Integer, ForeignKey('delivery.address.address_id'))
    dropoff_date = Column(Date, nullable=False)
    dropoff_time = Column(Time)
    creator_id = Column(Integer, ForeignKey('staff.staff.staff_id'), nullable=False)
    notes = Column(Text)
    attachments = Column(Integer, ForeignKey('delivery.attachment.attachment_id'))
    job_number = Column(Text)
    pickup_complete = Column(DateTime)
    dropoff_complete = Column(DateTime)
    created = Column(DateTime, default=datetime.utcnow)
    completion = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    pickup_address = relationship("Address", foreign_keys=[pickup_address_id])
    dropoff_address = relationship("Address", foreign_keys=[dropoff_address_id])
    creator = relationship("Staff")
    
    def __repr__(self):
        return f"<Booking(booking_id={self.booking_id}, pickup_date='{self.pickup_date}', dropoff_date='{self.dropoff_date}', completion={self.completion})>"


class Attachment(Base):
    """Attachment schema for storing file attachments"""
    __tablename__ = 'attachment'
    __table_args__ = {'schema': 'delivery'}
    
    attachment_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('delivery.booking.booking_id'))
    dropbox_path = Column(Text)
    dropbox_shared_url = Column(Text)
    uploaded_by = Column(Integer, ForeignKey('staff.staff.staff_id'))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    booking = relationship("Booking", foreign_keys=[booking_id])
    uploader = relationship("Staff", foreign_keys=[uploaded_by])
    
    def __repr__(self):
        return f"<Attachment(attachment_id={self.attachment_id}, booking_id={self.booking_id})>"

