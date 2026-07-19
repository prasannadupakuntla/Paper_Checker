import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.schemas.response import UploadResponse

router = APIRouter()

UPLOAD_DIR = "backend/uploads"

@router.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".pdf"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {ext}. Only JPG, JPEG, PNG, and PDF are supported."
        )

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate a unique image ID
    image_id = str(uuid.uuid4())
    filename = f"{image_id}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded file: {str(e)}"
        )

    return UploadResponse(image_id=image_id)
