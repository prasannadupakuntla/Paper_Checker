from pydantic import BaseModel
from typing import Optional

class EvaluationRequest(BaseModel):
    image_id: str
    student_id: Optional[str] = None

