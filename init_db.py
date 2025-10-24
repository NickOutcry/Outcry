#!/usr/bin/env python3
"""
Database initialization script
Creates tables and optionally populates with sample data
"""

from database import init_database, SessionLocal
from models import Client, Contact, Billing, ProductCategory, Product, ProductVariable, VariableOption, Staff, Project, Job, Item, ItemVariable, ItemVariableOption, JobStatus, JobStatusHistory
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    
    try:
        # Create sample clients
        clients = [
            Client(
                name="Smith Enterprises",
                address="123 Business Street",
                suburb="CBD",
                state="NSW",
                postcode=2000
            ),
            Client(
                name="Doe Industries",
                address="456 Industrial Way",
                suburb="Westside",
                state="VIC",
                postcode=3000
            ),
            Client(
                name="Johnson Corp",
                address="789 Corporate Blvd",
                suburb="Northside",
                state="QLD",
                postcode=4000
            )
        ]
        
        for client in clients:
            db.add(client)
        db.commit()
        
        # Create sample contacts
        contacts = [
            Contact(
                first_name="John",
                surname="Smith",
                email="john.smith@example.com",
                phone="555-0101",
                client_id=1
            ),
            Contact(
                first_name="Jane",
                surname="Doe",
                email="jane.doe@example.com",
                phone="555-0102",
                client_id=2
            ),
            Contact(
                first_name="Bob",
                surname="Johnson",
                email="bob.johnson@example.com",
                phone="555-0103",
                client_id=3
            )
        ]
        
        for contact in contacts:
            db.add(contact)
        db.commit()
        
        # Create sample billing
        billing = [
            Billing(
                entity="Smith Enterprises Pty Ltd",
                address="123 Business Street",
                suburb="CBD",
                state="NSW",
                postcode=2000,
                client_id=1
            ),
            Billing(
                entity="Doe Industries Ltd",
                address="456 Industrial Way",
                suburb="Westside",
                state="VIC",
                postcode=3000,
                client_id=2
            ),
            Billing(
                entity="Johnson Corporation",
                address="789 Corporate Blvd",
                suburb="Northside",
                state="QLD",
                postcode=4000,
                client_id=3
            )
        ]
        
        for bill in billing:
            db.add(bill)
        db.commit()
        
        # Create sample product categories
        categories = [
            ProductCategory(name="Widgets"),
            ProductCategory(name="Gadgets"),
            ProductCategory(name="Tools"),
            ProductCategory(name="Electronics")
        ]
        
        for category in categories:
            db.add(category)
        db.commit()
        
        # Create sample products
        products = [
            Product(
                name="Premium Widget",
                base_cost=45.00,
                multiplier_cost=2.2,
                product_category_id=1
            ),
            Product(
                name="Standard Gadget",
                base_cost=12.00,
                multiplier_cost=2.5,
                product_category_id=2
            ),
            Product(
                name="Deluxe Tool Set",
                base_cost=85.00,
                multiplier_cost=2.35,
                product_category_id=3
            ),
            Product(
                name="Smart Device",
                base_cost=150.00,
                multiplier_cost=1.8,
                product_category_id=4
            )
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        
        # Create sample product variables
        variables = [
            ProductVariable(
                name="Size",
                base_cost=0.00,
                multiplier_cost=1.0,
                data_type="select",
                product_id=1
            ),
            ProductVariable(
                name="Color",
                base_cost=5.00,
                multiplier_cost=1.1,
                data_type="select",
                product_id=1
            ),
            ProductVariable(
                name="Material",
                base_cost=10.00,
                multiplier_cost=1.2,
                data_type="select",
                product_id=2
            ),
            ProductVariable(
                name="Warranty",
                base_cost=15.00,
                multiplier_cost=1.15,
                data_type="select",
                product_id=3
            )
        ]
        
        for variable in variables:
            db.add(variable)
        db.commit()
        
        # Create sample variable options
        options = [
            VariableOption(
                name="Small",
                base_cost=0.00,
                multiplier_cost=1.0,
                product_variable_id=1
            ),
            VariableOption(
                name="Medium",
                base_cost=10.00,
                multiplier_cost=1.1,
                product_variable_id=1
            ),
            VariableOption(
                name="Large",
                base_cost=20.00,
                multiplier_cost=1.2,
                product_variable_id=1
            ),
            VariableOption(
                name="Red",
                base_cost=5.00,
                multiplier_cost=1.0,
                product_variable_id=2
            ),
            VariableOption(
                name="Blue",
                base_cost=5.00,
                multiplier_cost=1.0,
                product_variable_id=2
            ),
            VariableOption(
                name="Green",
                base_cost=8.00,
                multiplier_cost=1.1,
                product_variable_id=2
            ),
            VariableOption(
                name="Plastic",
                base_cost=0.00,
                multiplier_cost=1.0,
                product_variable_id=3
            ),
            VariableOption(
                name="Metal",
                base_cost=10.00,
                multiplier_cost=1.2,
                product_variable_id=3
            ),
            VariableOption(
                name="1 Year",
                base_cost=0.00,
                multiplier_cost=1.0,
                product_variable_id=4
            ),
            VariableOption(
                name="3 Years",
                base_cost=15.00,
                multiplier_cost=1.15,
                product_variable_id=4
            ),
            VariableOption(
                name="5 Years",
                base_cost=30.00,
                multiplier_cost=1.3,
                product_variable_id=4
            )
        ]
        
        for option in options:
            db.add(option)
        db.commit()
        
        # Create sample staff
        staff_members = [
            Staff(
                first_name="Alice",
                surname="Wilson",
                phone="555-0201",
                address="123 Staff Street",
                suburb="Staff Suburb",
                state="NSW",
                postcode=2000,
                dob=datetime(1990, 5, 15).date(),
                emergency_contact="John Wilson",
                emergency_contact_number="555-0301"
            ),
            Staff(
                first_name="Charlie",
                surname="Brown",
                phone="555-0202",
                address="456 Employee Ave",
                suburb="Employee Town",
                state="VIC",
                postcode=3000,
                dob=datetime(1985, 8, 22).date(),
                emergency_contact="Sarah Brown",
                emergency_contact_number="555-0302"
            ),
            Staff(
                first_name="Diana",
                surname="Prince",
                phone="555-0203",
                address="789 Worker Blvd",
                suburb="Worker City",
                state="QLD",
                postcode=4000,
                dob=datetime(1992, 3, 10).date(),
                emergency_contact="Steve Prince",
                emergency_contact_number="555-0303"
            )
        ]
        
        for staff in staff_members:
            db.add(staff)
        db.commit()
        
        # Create sample projects
        projects = [
            Project(
                name="Office Building Renovation",
                address="123 Business Street",
                suburb="CBD",
                state="NSW",
                postcode=2000,
                date_created=datetime.now().date()
            ),
            Project(
                name="Warehouse Installation",
                address="456 Industrial Way",
                suburb="Westside",
                state="VIC",
                postcode=3000,
                date_created=datetime.now().date()
            ),
            Project(
                name="Retail Store Setup",
                address="789 Shopping Center",
                suburb="Northside",
                state="QLD",
                postcode=4000,
                date_created=datetime.now().date()
            )
        ]
        
        for project in projects:
            db.add(project)
        db.commit()
        
        # Create sample jobs
        jobs = [
            Job(
                reference="JOB-001",
                project_id=1,
                client_id=1,
                po="PO-2024-001",
                date_created=datetime.now().date(),
                cost_excl_gst=1500.00,
                cost_incl_gst=1650.00,
                contact_id=1,
                staff_id=1
            ),
            Job(
                reference="JOB-002",
                project_id=2,
                client_id=2,
                po="PO-2024-002",
                date_created=datetime.now().date(),
                cost_excl_gst=800.00,
                cost_incl_gst=880.00,
                contact_id=2,
                staff_id=2
            ),
            Job(
                reference="JOB-003",
                project_id=3,
                client_id=3,
                po="PO-2024-003",
                date_created=datetime.now().date(),
                cost_excl_gst=1200.00,
                cost_incl_gst=1320.00,
                contact_id=3,
                staff_id=3
            )
        ]
        
        for job in jobs:
            db.add(job)
        db.commit()
        
        # Create sample items
        items = [
            Item(
                job_id=1,
                product_id=1,
                notes="Premium quality widget for main entrance",
                quantity=2,
                cost_excl_gst=99.99,
                cost_incl_gst=109.99
            ),
            Item(
                job_id=1,
                product_id=2,
                notes="Standard gadgets for office areas",
                quantity=5,
                cost_excl_gst=29.99,
                cost_incl_gst=32.99
            ),
            Item(
                job_id=2,
                product_id=3,
                notes="Complete tool set for warehouse",
                quantity=1,
                cost_excl_gst=199.99,
                cost_incl_gst=219.99
            ),
            Item(
                job_id=3,
                product_id=4,
                notes="Smart devices for retail display",
                quantity=3,
                cost_excl_gst=150.00,
                cost_incl_gst=165.00
            )
        ]
        
        for item in items:
            db.add(item)
        db.commit()
        
        # Create sample job statuses
        job_statuses = [
            JobStatus(job_status="Pending"),
            JobStatus(job_status="In Progress"),
            JobStatus(job_status="Completed"),
            JobStatus(job_status="Cancelled"),
            JobStatus(job_status="On Hold")
        ]
        
        for status in job_statuses:
            db.add(status)
        db.commit()
        
        # Create sample job status history
        status_history = [
            JobStatusHistory(
                job_id=1,
                job_status_id=1,  # Pending
                date=datetime.now().date() - timedelta(days=30)
            ),
            JobStatusHistory(
                job_id=1,
                job_status_id=2,  # In Progress
                date=datetime.now().date() - timedelta(days=15)
            ),
            JobStatusHistory(
                job_id=2,
                job_status_id=1,  # Pending
                date=datetime.now().date() - timedelta(days=7)
            ),
            JobStatusHistory(
                job_id=3,
                job_status_id=1,  # Pending
                date=datetime.now().date() - timedelta(days=5)
            ),
            JobStatusHistory(
                job_id=3,
                job_status_id=2,  # In Progress
                date=datetime.now().date() - timedelta(days=2)
            )
        ]
        
        for history in status_history:
            db.add(history)
        db.commit()
        
        # Create sample item variables
        item_variables = [
            ItemVariable(
                item_id=1,
                product_variable_id=1  # Size variable for Premium Widget
            ),
            ItemVariable(
                item_id=1,
                product_variable_id=2  # Color variable for Premium Widget
            ),
            ItemVariable(
                item_id=2,
                product_variable_id=3  # Material variable for Standard Gadget
            ),
            ItemVariable(
                item_id=3,
                product_variable_id=4  # Warranty variable for Deluxe Tool Set
            )
        ]
        
        for item_var in item_variables:
            db.add(item_var)
        db.commit()
        
        # Create sample item variable options
        item_variable_options = [
            ItemVariableOption(
                item_variable_id=1,
                variable_option_id=2  # Medium size
            ),
            ItemVariableOption(
                item_variable_id=2,
                variable_option_id=4  # Red color
            ),
            ItemVariableOption(
                item_variable_id=3,
                variable_option_id=8  # Metal material
            ),
            ItemVariableOption(
                item_variable_id=4,
                variable_option_id=10  # 3 Years warranty
            )
        ]
        
        for item_var_opt in item_variable_options:
            db.add(item_var_opt)
        db.commit()
        
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    
    # Ask user if they want sample data
    response = input("Do you want to create sample data? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        create_sample_data()
    
    print("Database setup complete!")
