"""
Public schema models
General/system tables that don't belong to specific domains
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base


# Note: The public schema typically contains system tables, enums, or general-purpose tables
# Add models here as needed for tables in the 'public' schema
# Example structure below - adjust based on your actual database schema

# If you have specific tables in the public schema, add them here following the pattern:
# class YourTable(Base):
#     """Your table description"""
#     __tablename__ = 'your_table'
#     __table_args__ = {'schema': 'public'}
#     
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     # ... other columns
#     
#     def __repr__(self):
#         return f"<YourTable(id={self.id})>"

