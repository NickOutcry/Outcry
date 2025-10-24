from database import engine, SessionLocal
from models import Client, Contact, Project, Staff, Job, JobStatus
from datetime import datetime

print('Adding sample data for jobs testing...')
try:
    db = SessionLocal()
    
    # Add sample client
    client = Client(
        name="Test Client for Jobs",
        address="123 Test Street",
        suburb="Test Suburb",
        state="NSW",
        postcode=2000
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    print(f'✅ Added client: {client.name} (ID: {client.client_id})')
    
    # Add sample contact
    contact = Contact(
        first_name="John",
        surname="Doe",
        email="john.doe@test.com",
        phone="123456789",
        client_id=client.client_id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    print(f'✅ Added contact: {contact.first_name} {contact.surname} (ID: {contact.contact_id})')
    
    # Add sample project
    project = Project(
        name="Test Project",
        address="456 Project Street",
        suburb="Project Suburb",
        state="NSW",
        postcode=2000
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    print(f'✅ Added project: {project.name} (ID: {project.project_id})')
    
    # Add sample staff
    staff = Staff(
        first_name="Jane",
        surname="Smith",
        phone="987654321",
        address="789 Staff Street",
        suburb="Staff Suburb",
        state="NSW",
        postcode=2000
    )
    db.add(staff)
    db.commit()
    db.refresh(staff)
    print(f'✅ Added staff: {staff.first_name} {staff.surname} (ID: {staff.staff_id})')
    
    # Add sample job
    job = Job(
        reference="JOB-001",
        project_id=project.project_id,
        client_id=client.client_id,
        contact_id=contact.contact_id,
        staff_id=staff.staff_id,
        job_status_id=1,  # Quote status
        po="PO-2025-001",
        date_created=datetime.now().date()
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    print(f'✅ Added job: {job.reference} (ID: {job.job_id})')
    
    print('\n✅ All sample data added successfully!')
    
except Exception as e:
    print('❌ Error adding sample data:', e)
    db.rollback()
finally:
    db.close()
