import os
from backend.services.preprocessing.image_processor import ImagePreprocessor
from backend.services.ocr.paddle_service import PaddleOCRService

def test_ocr_extraction():
    processor = ImagePreprocessor()
    ocr = PaddleOCRService()
    
    assert os.path.exists("tests/handwritten.jpeg"), "Handwritten sample image not found."
    
    processed = processor.process("tests/handwritten.jpeg")
    result = ocr.extract_text(processed.processed_path)
    
    assert result is not None
    assert result.average_confidence >= 0.0
    assert len(result.text) > 0