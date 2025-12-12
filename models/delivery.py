"""
Delivery domain models
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, Numeric, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base


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
    
    # Relationships
    pickup_bookings = relationship("Booking", foreign_keys="[Booking.pickup_address_id]", back_populates="pickup_address")
    dropoff_bookings = relationship("Booking", foreign_keys="[Booking.dropoff_address_id]", back_populates="dropoff_address")
    
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
    pickup_address = relationship("Address", foreign_keys=[pickup_address_id], back_populates="pickup_bookings")
    dropoff_address = relationship("Address", foreign_keys=[dropoff_address_id], back_populates="dropoff_bookings")
    creator = relationship("Staff")
    booking_attachments = relationship("Attachment", foreign_keys="[Attachment.booking_id]", back_populates="booking")
    
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
    booking = relationship("Booking", foreign_keys=[booking_id], back_populates="booking_attachments")
    uploader = relationship("Staff", foreign_keys=[uploaded_by])
    
    def __repr__(self):
        return f"<Attachment(attachment_id={self.attachment_id}, booking_id={self.booking_id})>"

