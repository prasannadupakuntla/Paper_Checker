from fastapi import APIRouter, HTTPException
from backend.schemas.request import EvaluationRequest
from backend.schemas.response import EvaluationResponse
from backend.engine.pipeline import EvaluationPipeline

router = APIRouter()
pipeline = EvaluationPipeline()

@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate_image(request: EvaluationRequest):
    try:
        result = pipeline.run(request.image_id)
        return EvaluationResponse(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
