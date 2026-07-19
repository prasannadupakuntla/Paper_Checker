from abc import ABC, abstractmethod

class EvaluationService(ABC):
    @abstractmethod
    def evaluate_answer(self, corrected_ocr: str) -> dict:
        """
        Evaluate corrected OCR text against a rubric.
        Returns a dictionary containing:
            - score (float)
            - rubric (str)
            - evaluation (str)
            - feedback (str)
            - concepts (list[str])
        """
        pass
