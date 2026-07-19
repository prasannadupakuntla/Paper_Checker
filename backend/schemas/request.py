from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    image_id: str
