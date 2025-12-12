"""
Client domain router - Client, Contact, Billing CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models.client import Client, Contact, Billing
from schemas.client import (
    ClientBase, ClientCreate, ClientRead,
    ContactBase, ContactCreate, ContactRead,
    BillingBase, BillingCreate, BillingRead
)
from typing import Optional
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["client"])


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# CLIENT ROUTES
# ============================================================================

@router.get("/clients", response_model=List[ClientRead])
async def get_clients(db: Session = Depends(get_db)):
    """Get all clients with their contacts and billing entities"""
    clients = db.query(Client).all()
    result = []
    for client in clients:
        client_data = {
            "client_id": client.client_id,
            "name": client.name,
            "address": client.address,
            "suburb": client.suburb,
            "state": client.state,
            "postcode": client.postcode,
            "contacts": [],
            "billing": []
        }
        for contact in client.contacts:
            client_data["contacts"].append({
                "contact_id": contact.contact_id,
                "first_name": contact.first_name,
                "surname": contact.surname,
                "email": contact.email,
                "phone": contact.phone,
                "client_id": contact.client_id
            })
        for bill in client.billing:
            client_data["billing"].append({
                "billing_id": bill.billing_id,
                "entity": bill.entity,
                "address": bill.address,
                "suburb": bill.suburb,
                "state": bill.state,
                "postcode": bill.postcode
            })
        result.append(client_data)
    return result


@router.get("/clients/{client_id}", response_model=ClientRead)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    """Get a single client by ID"""
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/clients", response_model=ClientRead, status_code=201)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Create a new client"""
    try:
        new_client = Client(
            name=client.name,
            address=client.address,
            suburb=client.suburb,
            state=client.state,
            postcode=client.postcode
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/clients/{client_id}", response_model=ClientRead)
async def update_client(
    client_id: int,
    client_update: ClientBase,
    db: Session = Depends(get_db)
):
    """Update an existing client"""
    try:
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        if client_update.name is not None:
            client.name = client_update.name
        if client_update.address is not None:
            client.address = client_update.address
        if client_update.suburb is not None:
            client.suburb = client_update.suburb
        if client_update.state is not None:
            client.state = client_update.state
        if client_update.postcode is not None:
            client.postcode = client_update.postcode
        
        db.commit()
        db.refresh(client)
        return client
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/clients/{client_id}", status_code=204)
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Delete a client"""
    try:
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        db.delete(client)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# CONTACT ROUTES
# ============================================================================

@router.get("/contacts", response_model=List[ContactRead])
async def get_contacts(client_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all contacts, optionally filtered by client_id"""
    query = db.query(Contact)
    if client_id:
        query = query.filter(Contact.client_id == client_id)
    contacts = query.all()
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactRead)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get a single contact by ID"""
    contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/contacts", response_model=ContactRead, status_code=201)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """Create a new contact"""
    try:
        new_contact = Contact(
            first_name=contact.first_name,
            surname=contact.surname,
            email=contact.email,
            phone=contact.phone,
            client_id=contact.client_id
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/contacts/{contact_id}", response_model=ContactRead)
async def update_contact(
    contact_id: int,
    contact_update: ContactBase,
    db: Session = Depends(get_db)
):
    """Update an existing contact"""
    try:
        contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        if contact_update.first_name is not None:
            contact.first_name = contact_update.first_name
        if contact_update.surname is not None:
            contact.surname = contact_update.surname
        if contact_update.email is not None:
            contact.email = contact_update.email
        if contact_update.phone is not None:
            contact.phone = contact_update.phone
        
        db.commit()
        db.refresh(contact)
        return contact
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/contacts/{contact_id}", status_code=204)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact"""
    try:
        contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        db.delete(contact)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# BILLING ROUTES
# ============================================================================

@router.get("/billing", response_model=List[BillingRead])
async def get_billing_entities(
    client_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all billing entities, optionally filtered by client_id"""
    query = db.query(Billing)
    if client_id:
        query = query.filter(Billing.client_id == client_id)
    billing_entities = query.all()
    return billing_entities


@router.get("/billing/{billing_id}", response_model=BillingRead)
async def get_billing_entity(billing_id: int, db: Session = Depends(get_db)):
    """Get a single billing entity by ID"""
    billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing entity not found")
    return billing


@router.post("/billing", response_model=BillingRead, status_code=201)
async def create_billing_entity(billing: BillingCreate, db: Session = Depends(get_db)):
    """Create a new billing entity"""
    try:
        new_billing = Billing(
            entity=billing.entity,
            address=billing.address,
            suburb=billing.suburb,
            state=billing.state,
            postcode=billing.postcode,
            client_id=billing.client_id
        )
        db.add(new_billing)
        db.commit()
        db.refresh(new_billing)
        return new_billing
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/billing/{billing_id}", response_model=BillingRead)
async def update_billing_entity(
    billing_id: int,
    billing_update: BillingBase,
    db: Session = Depends(get_db)
):
    """Update an existing billing entity"""
    try:
        billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
        if not billing:
            raise HTTPException(status_code=404, detail="Billing entity not found")
        
        if billing_update.entity is not None:
            billing.entity = billing_update.entity
        if billing_update.address is not None:
            billing.address = billing_update.address
        if billing_update.suburb is not None:
            billing.suburb = billing_update.suburb
        if billing_update.state is not None:
            billing.state = billing_update.state
        if billing_update.postcode is not None:
            billing.postcode = billing_update.postcode
        
        db.commit()
        db.refresh(billing)
        return billing
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/billing/{billing_id}", status_code=204)
async def delete_billing_entity(billing_id: int, db: Session = Depends(get_db)):
    """Delete a billing entity"""
    try:
        billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
        if not billing:
            raise HTTPException(status_code=404, detail="Billing entity not found")
        
        db.delete(billing)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/clients/{client_id}/billing-entities", response_model=List[BillingRead])
async def get_client_billing_entities(client_id: int, db: Session = Depends(get_db)):
    """Get all billing entities for a specific client"""
    billing_entities = db.query(Billing).filter(Billing.client_id == client_id).all()
    return billing_entities



# ============================================================================
# TEST ENDPOINT
# ============================================================================

@router.get("/client/test", response_class=JSONResponse)
async def test_client_connection(db: Session = Depends(get_db)):
    """
    Test endpoint to verify database connection and models.
    Returns the first record from Client, Contact, and Billing tables.
    """
    result = {
        "status": "success",
        "message": "Database connection and models are working",
        "data": {}
    }
    
    try:
        # Test Client table
        first_client = db.query(Client).first()
        if first_client:
            result["data"]["client"] = {
                "client_id": first_client.client_id,
                "name": first_client.name,
                "address": first_client.address,
                "suburb": first_client.suburb,
                "state": first_client.state,
                "postcode": first_client.postcode
            }
        else:
            result["data"]["client"] = None
        
        # Test Contact table
        first_contact = db.query(Contact).first()
        if first_contact:
            result["data"]["contact"] = {
                "contact_id": first_contact.contact_id,
                "first_name": first_contact.first_name,
                "surname": first_contact.surname,
                "email": first_contact.email,
                "phone": first_contact.phone,
                "client_id": first_contact.client_id
            }
        else:
            result["data"]["contact"] = None
        
        # Test Billing table
        first_billing = db.query(Billing).first()
        if first_billing:
            result["data"]["billing"] = {
                "billing_id": first_billing.billing_id,
                "entity": first_billing.entity,
                "address": first_billing.address,
                "suburb": first_billing.suburb,
                "state": first_billing.state,
                "postcode": first_billing.postcode,
                "client_id": first_billing.client_id
            }
        else:
            result["data"]["billing"] = None
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}",
            "data": {}
        }
