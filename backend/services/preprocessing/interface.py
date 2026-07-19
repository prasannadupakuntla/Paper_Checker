from abc import ABC, abstractmethod

from .image_models import ProcessedImage


class ImageProcessor(ABC):

    @abstractmethod
    def process(self, image_path: str) -> ProcessedImage:
        """
        Process an image before OCR.
        """
        pass