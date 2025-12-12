"""
File upload router - Handles file uploads to Dropbox
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from database import SessionLocal
from models.delivery import Attachment
from schemas.delivery import AttachmentRead as AttachmentResponse

# Try to import dropbox_service, but make it optional
try:
    from dropbox_service import get_dropbox_service, upload_multiple_files
    DROPBOX_AVAILABLE = True
except ImportError:
    DROPBOX_AVAILABLE = False
    print("Warning: dropbox_service not available")

router = APIRouter(prefix="/api", tags=["upload"])


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=List[AttachmentResponse])
async def upload_files(
    files: List[UploadFile] = File(...),
    entity_id: int = Form(...),
    entity_type: str = Form("general"),
    uploaded_by: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload files to Dropbox
    
    - **files**: List of files to upload
    - **entity_id**: ID of the entity (job_id, booking_id, etc.)
    - **entity_type**: Type of entity ('job', 'booking', 'general', etc.)
    - **uploaded_by**: ID of the user uploading the files (optional)
    
    Returns list of uploaded file information with Dropbox paths and shared URLs
    """
    if not DROPBOX_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Dropbox service not available. Please check configuration."
        )
    
    if not files or all(not file.filename for file in files):
        raise HTTPException(status_code=400, detail="No files provided")
    
    try:
        # Prepare files for upload
        files_to_upload = []
        for file in files:
            if file.filename:
                file_content = await file.read()
                files_to_upload.append({
                    "content": file_content,
                    "filename": file.filename
                })
        
        if not files_to_upload:
            raise HTTPException(status_code=400, detail="No valid files to upload")
        
        # Upload files to Dropbox
        dropbox_service = get_dropbox_service()
        upload_results = upload_multiple_files(
            files_to_upload,
            entity_id,
            entity_type
        )
        
        if not upload_results:
            raise HTTPException(
                status_code=500,
                detail="Failed to upload files to Dropbox"
            )
        
        # Save attachment records to database
        attachments = []
        for result in upload_results:
            attachment = Attachment(
                booking_id=entity_id if entity_type == "booking" else None,
                dropbox_path=result["dropbox_path"],
                dropbox_shared_url=result["dropbox_shared_url"],
                uploaded_by=uploaded_by or 1  # Default to staff ID 1
            )
            db.add(attachment)
            attachments.append(attachment)
        
        db.commit()
        
        # Refresh to get attachment IDs
        for attachment in attachments:
            db.refresh(attachment)
        
        return [
            {
                "attachment_id": att.attachment_id,
                "booking_id": att.booking_id,
                "dropbox_path": att.dropbox_path,
                "dropbox_shared_url": att.dropbox_shared_url,
                "uploaded_by": att.uploaded_by,
                "uploaded_at": att.uploaded_at.isoformat() if att.uploaded_at else None
            }
            for att in attachments
        ]
    
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload files: {str(e)}"
        )


@router.post("/upload/job/{job_id}", response_model=List[AttachmentResponse])
async def upload_job_files(
    job_id: int,
    files: List[UploadFile] = File(...),
    uploaded_by: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload files for a specific job
    
    - **job_id**: ID of the job
    - **files**: List of files to upload
    - **uploaded_by**: ID of the user uploading the files (optional)
    """
    return await upload_files(
        files=files,
        entity_id=job_id,
        entity_type="job",
        uploaded_by=uploaded_by,
        db=db
    )


@router.post("/upload/booking/{booking_id}", response_model=List[AttachmentResponse])
async def upload_booking_files(
    booking_id: int,
    files: List[UploadFile] = File(...),
    uploaded_by: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload files for a specific booking
    
    - **booking_id**: ID of the booking
    - **files**: List of files to upload
    - **uploaded_by**: ID of the user uploading the files (optional)
    """
    return await upload_files(
        files=files,
        entity_id=booking_id,
        entity_type="booking",
        uploaded_by=uploaded_by,
        db=db
    )


@router.get("/attachments", response_model=List[AttachmentResponse])
async def get_attachments(
    booking_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all attachments, optionally filtered by booking_id"""
    query = db.query(Attachment)
    if booking_id:
        query = query.filter(Attachment.booking_id == booking_id)
    attachments = query.all()
    
    return [
        {
            "attachment_id": att.attachment_id,
            "booking_id": att.booking_id,
            "dropbox_path": att.dropbox_path,
            "dropbox_shared_url": att.dropbox_shared_url,
            "uploaded_by": att.uploaded_by,
            "uploaded_at": att.uploaded_at.isoformat() if att.uploaded_at else None
        }
        for att in attachments
    ]


@router.get("/attachments/{attachment_id}", response_model=AttachmentResponse)
async def get_attachment(attachment_id: int, db: Session = Depends(get_db)):
    """Get a single attachment by ID"""
    attachment = db.query(Attachment).filter(
        Attachment.attachment_id == attachment_id
    ).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    return {
        "attachment_id": attachment.attachment_id,
        "booking_id": attachment.booking_id,
        "dropbox_path": attachment.dropbox_path,
        "dropbox_shared_url": attachment.dropbox_shared_url,
        "uploaded_by": attachment.uploaded_by,
        "uploaded_at": attachment.uploaded_at.isoformat() if attachment.uploaded_at else None
    }


@router.delete("/attachments/{attachment_id}", status_code=204)
async def delete_attachment(attachment_id: int, db: Session = Depends(get_db)):
    """Delete an attachment"""
    try:
        attachment = db.query(Attachment).filter(
            Attachment.attachment_id == attachment_id
        ).first()
        if not attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        
        # Optionally delete from Dropbox
        if DROPBOX_AVAILABLE and attachment.dropbox_path:
            try:
                from dropbox_service import delete_file
                delete_file(attachment.dropbox_path)
            except Exception as e:
                print(f"Error deleting file from Dropbox: {str(e)}")
                # Continue with database deletion even if Dropbox deletion fails
        
        db.delete(attachment)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

