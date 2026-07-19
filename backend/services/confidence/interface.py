from abc import ABC, abstractmethod
from backend.services.ocr.ocr_models import OCRResult

class ConfidenceService(ABC):
    @abstractmethod
    def calculate_confidence(self, ocr_result: OCRResult) -> float:
        """
        Calculate and return a confidence score (float, 0-100) for the OCR extraction.
        """
        pass
