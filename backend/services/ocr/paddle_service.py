from __future__ import annotations

import logging
from statistics import mean

from paddleocr import PaddleOCR

from .interface import OCRService
from .ocr_models import OCRResult, OCRLine

logger = logging.getLogger(__name__)


class PaddleOCRService(OCRService):
    """
    PaddleOCR implementation.

    Responsibilities:
        - Load the OCR model once
        - Extract text from an image
        - Convert PaddleOCR output into our internal schema

    Responsibilities it DOES NOT have:
        - Calibration
        - OCR correction
        - Question detection
        - RAG
        - Evaluation
    """

    def __init__(
        self,
        language: str = "en",
        use_angle_cls: bool = True,
        use_gpu: bool = False,
    ) -> None:

        self.use_angle_cls = use_angle_cls

        logger.info("Initializing PaddleOCR...")

        self.ocr = PaddleOCR(
            lang=language,
            use_angle_cls=use_angle_cls,
            use_gpu=use_gpu,
        )

        logger.info("PaddleOCR initialized successfully.")

    def extract_text(self, image_path: str) -> OCRResult:
        """
        Run OCR on an image.

        Args:
            image_path: Path to the input image.

        Returns:
            OCRResult
        """

        try:

            raw_result = self.ocr.ocr(
                image_path,
                cls=self.use_angle_cls,
            )

        except Exception as e:
            logger.exception("OCR failed.")
            raise RuntimeError(f"OCR failed: {e}") from e

        return self._parse_result(raw_result)

    def _parse_result(self, raw_result) -> OCRResult:
        """
        Convert PaddleOCR output into OCRResult.
        """

        if (
            not raw_result
            or len(raw_result) == 0
            or raw_result[0] is None
        ):
            return OCRResult(
                text="",
                lines=[],
                average_confidence=0.0,
            )

        lines: list[OCRLine] = []

        confidences = []

        for detection in raw_result[0]:

            bounding_box = detection[0]

            text = detection[1][0]

            confidence = float(detection[1][1])

            confidences.append(confidence)

            lines.append(
                OCRLine(
                    text=text,
                    confidence=confidence,
                    box=bounding_box,
                )
            )

        full_text = "\n".join(
            line.text
            for line in lines
        )

        average_confidence = (
            mean(confidences)
            if confidences
            else 0.0
        )

        logger.info(
            "OCR extracted %d lines (avg confidence %.2f)",
            len(lines),
            average_confidence,
        )

        return OCRResult(
            text=full_text,
            lines=lines,
            average_confidence=average_confidence,
        )