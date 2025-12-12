"""
Staff domain models
"""
from sqlalchemy import Column, Integer, Text, Date
from sqlalchemy.orm import relationship
from . import Base


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

