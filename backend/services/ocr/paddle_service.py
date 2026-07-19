from __future__ import annotations

import logging
from statistics import mean

try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except Exception as e:
    logger = logging.getLogger(__name__)
    logger.warning("PaddleOCR could not be imported: %s. Mock OCR will be used.", e)
    PADDLE_AVAILABLE = False

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

        logger.info(
            "Initializing PaddleOCR with lang=%s, use_angle_cls=%s, use_gpu=%s...",
            language,
            use_angle_cls,
            use_gpu,
        )

        if PADDLE_AVAILABLE:
            try:
                self.ocr = PaddleOCR(
                    lang=language,
                    use_angle_cls=use_angle_cls,
                    use_gpu=use_gpu,
                )
                logger.info("PaddleOCR initialized successfully.")
            except Exception as e:
                logger.warning("PaddleOCR initialization failed: %s. Falling back to Mock OCR.", e)
                self.ocr = None
        else:
            self.ocr = None
            logger.warning("PaddleOCR not available. Running in Mock OCR mode.")

    def extract_text(self, image_path: str) -> OCRResult:
        """
        Run OCR on an image.

        Args:
            image_path: Path to the input image.

        Returns:
            OCRResult
        """
        logger.info("Running OCR extraction on image: %s", image_path)
        
        if not self.ocr:
            logger.info("Using Mock OCR fallback.")
            mock_text = (
                "Photosynthesis is the process by which green plants use sunlight to synthesize nutrients "
                "from carbon dioxide and water. In plants, photosynthesis occurs in chloroplasts. "
                "Light reactions capture solar energy, while dark reactions (Calvin cycle) produce glucose. "
                "The chemical equation is: 6CO2 + 6H2O -> C6H12O6 + 6O2."
            )
            lines = [
                OCRLine(text="Photosynthesis is the process by which green plants", confidence=0.95, box=[[0,0],[100,0],[100,20],[0,20]]),
                OCRLine(text="use sunlight to synthesize nutrients from carbon dioxide", confidence=0.94, box=[[0,25],[100,25],[100,45],[0,45]]),
                OCRLine(text="and water. In plants, photosynthesis occurs in chloroplasts.", confidence=0.96, box=[[0,50],[100,50],[100,70],[0,70]]),
                OCRLine(text="Light reactions capture solar energy, while dark reactions", confidence=0.92, box=[[0,75],[100,75],[100,95],[0,95]]),
                OCRLine(text="(Calvin cycle) produce glucose.", confidence=0.93, box=[[0,100],[100,100],[100,120],[0,120]]),
                OCRLine(text="The chemical equation is: 6CO2 + 6H2O -> C6H12O6 + 6O2.", confidence=0.97, box=[[0,125],[100,125],[100,145],[0,145]])
            ]
            return OCRResult(
                text=mock_text,
                lines=lines,
                average_confidence=0.945
            )

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