"""
Client domain models
"""
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


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

