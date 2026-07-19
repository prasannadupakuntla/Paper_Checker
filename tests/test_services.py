import pytest
from backend.services.ocr.ocr_models import OCRResult, OCRLine
from backend.services.evaluation.service import RubricEvaluationService
from backend.services.confidence.service import TextConfidenceService
from backend.services.rag.service import KeywordRAGService

def test_evaluation_service():
    service = RubricEvaluationService()
    
    # 1. Full match
    text = "Photosynthesis is the process in green plants using light reactions and dark reactions and the equation co2 + h2o."
    res = service.evaluate_answer(text)
    assert res["score"] == 8.5
    assert "Photosynthesis Definition" in res["concepts"]
    assert "Light/Dark Reactions" in res["concepts"]
    assert "Chemical Equation" in res["concepts"]
    
    # 2. No match fallback
    text_empty = "Something random"
    res_empty = service.evaluate_answer(text_empty)
    assert res_empty["score"] == 5.0
    assert "General Biology Concepts" in res_empty["concepts"]

def test_confidence_service():
    service = TextConfidenceService()
    
    # Non-zero confidence
    ocr = OCRResult(text="Hello", lines=[], average_confidence=0.88)
    assert service.calculate_confidence(ocr) == 88.0
    
    # Zero confidence fallback
    ocr_zero = OCRResult(text="", lines=[], average_confidence=0.0)
    assert service.calculate_confidence(ocr_zero) == 85.0

def test_rag_service():
    service = KeywordRAGService()
    
    # Match specific concepts
    text = "chloroplasts light reactions equation"
    concepts = service.retrieve_concepts(text)
    assert "Light/Dark Reactions" in concepts
    assert "Chemical Equation" in concepts
    
    # Fallback concept
    concepts_empty = service.retrieve_concepts("random query")
    assert concepts_empty == "General Biology Concepts"
