import os
import logging
from fastapi import APIRouter, HTTPException

from backend.schemas.calibration_schemas import CalibrateRequest, CalibrateResponse
from backend.services.preprocessing.image_processor import ImagePreprocessor
from backend.services.ocr.paddle_service import PaddleOCRService
from backend.services.calibration.service import FileCalibrationService
from backend.services.calibration.config import DEFAULT_REFERENCE_TEXT

router = APIRouter()
logger = logging.getLogger(__name__)

preprocessor = ImagePreprocessor()
ocr_service = PaddleOCRService()
calibration_service = FileCalibrationService()

@router.post("/calibrate", response_model=CalibrateResponse)
def calibrate_student(request: CalibrateRequest):
    uploads_dir = "backend/uploads"
    
    # 1. Find the calibration image file
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir, exist_ok=True)
        
    matching_files = [f for f in os.listdir(uploads_dir) if f.startswith(request.image_id)]
    if not matching_files:
        raise HTTPException(
            status_code=404, 
            detail=f"Calibration image with ID {request.image_id} not found."
        )
    
    image_path = os.path.join(uploads_dir, matching_files[0])
    
    try:
        # 2. Preprocess the image
        logger.info("Calibrate API: Preprocessing image...")
        processed_image = preprocessor.process(image_path)
        
        # 3. Run OCR
        logger.info("Calibrate API: Running OCR...")
        ocr_result = ocr_service.extract_text(processed_image.processed_path)
        
        # 4. Calibrate Profile
        logger.info("Calibrate API: Performing calibration...")
        reference_text = request.reference_text or DEFAULT_REFERENCE_TEXT
        
        profile = calibration_service.calibrate(
            student_id=request.student_id,
            ocr_result=ocr_result,
            reference_text=reference_text
        )
        
        # 5. Save the profile
        calibration_service.save_profile(profile)
        
        return CalibrateResponse(
            student_id=request.student_id,
            profile=profile
        )
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Calibration endpoint failed.")
        raise HTTPException(status_code=500, detail=f"Calibration failed: {str(e)}")
