from abc import ABC, abstractmethod

from .ocr_models import OCRResult


class OCRService(ABC):

    @abstractmethod
    def extract_text(self, image_path: str) -> OCRResult:
        """
        Extract text from an image.
        """
        pass