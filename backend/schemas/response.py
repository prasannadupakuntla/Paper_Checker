from pydantic import BaseModel

class UploadResponse(BaseModel):
    image_id: str

class EvaluationResponse(BaseModel):
    image_id: str
    original_image_url: str
    ocr_text: str
    corrected_ocr: str
    retrieved_concept: str
    rubric: str
    evaluation: str
    confidence: float
    feedback: str
