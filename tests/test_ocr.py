from backend.services.preprocessing.image_processor import ImagePreprocessor
from backend.services.ocr.paddle_service import PaddleOCRService


processor = ImagePreprocessor()

ocr = PaddleOCRService()

processed = processor.process(
    "tests/handwritten.jpeg"
)

result = ocr.extract_text(
    processed.processed_path
)

print(result.model_dump_json(indent=4))