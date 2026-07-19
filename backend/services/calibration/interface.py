from abc import ABC, abstractmethod
from backend.services.ocr.ocr_models import OCRResult
from .calibration_models import HandwritingProfile

class CalibrationService(ABC):
    @abstractmethod
    def calibrate(self, student_id: str, ocr_result: OCRResult, reference_text: str) -> HandwritingProfile:
        """
        Calibrate the student's profile by comparing raw OCR result of the calibration sheet
        against the known expected reference text, extracting physical metrics and character confusions.
        """
        pass

    @abstractmethod
    def correct_ocr_result(self, ocr_result: OCRResult, profile: HandwritingProfile) -> OCRResult:
        """
        Apply the student's profile to correct low-confidence lines/words in the OCRResult.
        Returns a new OCRResult with corrected text and boosted confidence.
        """
        pass

    @abstractmethod
    def save_profile(self, profile: HandwritingProfile) -> None:
        """
        Persist the student's profile to the filesystem as a JSON file.
        """
        pass

    @abstractmethod
    def load_profile(self, student_id: str) -> HandwritingProfile | None:
        """
        Load the student's profile from the filesystem. Returns None if it doesn't exist.
        """
        pass
