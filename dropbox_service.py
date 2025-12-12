"""
Dropbox Service Module
Handles file uploads to Dropbox
"""
import dropbox
from typing import List, Dict, Optional
import os
from datetime import datetime

# Global Dropbox client instance
_dropbox_client: Optional[dropbox.Dropbox] = None


def initialize_dropbox_service(access_token: str):
    """Initialize Dropbox service with access token"""
    global _dropbox_client
    try:
        _dropbox_client = dropbox.Dropbox(access_token)
        # Test the connection
        _dropbox_client.users_get_current_account()
        print("Dropbox service initialized successfully")
    except Exception as e:
        print(f"Error initializing Dropbox service: {str(e)}")
        raise


def get_dropbox_service() -> dropbox.Dropbox:
    """Get the Dropbox service instance"""
    global _dropbox_client
    if _dropbox_client is None:
        raise RuntimeError("Dropbox service not initialized. Call initialize_dropbox_service() first.")
    return _dropbox_client


def upload_multiple_files(
    files: List[Dict[str, bytes]],
    entity_id: int,
    entity_type: str = "general"
) -> List[Dict[str, str]]:
    """
    Upload multiple files to Dropbox
    
    Args:
        files: List of dicts with 'content' (bytes) and 'filename' (str)
        entity_id: ID of the entity (job_id, booking_id, etc.)
        entity_type: Type of entity ('job', 'booking', 'general', etc.)
    
    Returns:
        List of dicts with 'dropbox_path' and 'dropbox_shared_url'
    """
    if not _dropbox_client:
        raise RuntimeError("Dropbox service not initialized")
    
    results = []
    base_path = f"/{entity_type}/{entity_id}"
    
    for file_info in files:
        filename = file_info.get("filename", "unnamed_file")
        content = file_info.get("content")
        
        if not content:
            continue
        
        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{timestamp}{ext}"
        dropbox_path = f"{base_path}/{unique_filename}"
        
        try:
            # Upload file to Dropbox
            _dropbox_client.files_upload(
                content,
                dropbox_path,
                mode=dropbox.files.WriteMode.overwrite
            )
            
            # Create shared link
            shared_link = _dropbox_client.sharing_create_shared_link_with_settings(
                dropbox_path
            )
            
            results.append({
                "dropbox_path": dropbox_path,
                "dropbox_shared_url": shared_link.url,
                "filename": filename
            })
        except Exception as e:
            print(f"Error uploading file {filename} to Dropbox: {str(e)}")
            # Continue with other files even if one fails
            continue
    
    return results


def upload_single_file(
    content: bytes,
    filename: str,
    entity_id: int,
    entity_type: str = "general"
) -> Dict[str, str]:
    """
    Upload a single file to Dropbox
    
    Args:
        content: File content as bytes
        filename: Original filename
        entity_id: ID of the entity
        entity_type: Type of entity
    
    Returns:
        Dict with 'dropbox_path' and 'dropbox_shared_url'
    """
    results = upload_multiple_files(
        [{"content": content, "filename": filename}],
        entity_id,
        entity_type
    )
    return results[0] if results else None


def delete_file(dropbox_path: str) -> bool:
    """
    Delete a file from Dropbox
    
    Args:
        dropbox_path: Path to the file in Dropbox
    
    Returns:
        True if successful, False otherwise
    """
    if not _dropbox_client:
        raise RuntimeError("Dropbox service not initialized")
    
    try:
        _dropbox_client.files_delete_v2(dropbox_path)
        return True
    except Exception as e:
        print(f"Error deleting file {dropbox_path} from Dropbox: {str(e)}")
        return False
