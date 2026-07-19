from pydantic import BaseModel
from typing import Optional
from backend.services.calibration.calibration_models import HandwritingProfile

class CalibrateRequest(BaseModel):
    student_id: str
    image_id: str
    reference_text: Optional[str] = None

class CalibrateResponse(BaseModel):
    student_id: str
    profile: HandwritingProfile
