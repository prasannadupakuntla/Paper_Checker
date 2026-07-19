from __future__ import annotations

import logging
import os

import cv2

from .config import ProcessingConfig
from .image_models import ProcessedImage
from .interface import ImageProcessor
from .validator import ImageValidator

logger = logging.getLogger(__name__)


class ImagePreprocessor(ImageProcessor):
    """
    Image preprocessing service.

    Responsibilities:
    - Read image
    - Validate image
    - Improve image quality for OCR
    - Save processed image

    Does NOT perform OCR.
    """

    def __init__(
        self,
        config: ProcessingConfig | None = None,
    ):
        self.config = config or ProcessingConfig()
        logger.info("Initialized ImagePreprocessor with config: %s", self.config)

    def process(self, image_path: str) -> ProcessedImage:
        logger.info("Starting image preprocessing for: %s", image_path)

        validator = ImageValidator()
        validator.validate(image_path)

        image = cv2.imread(image_path)

        if image is None:
            logger.error("Unable to read image: %s", image_path)
            raise FileNotFoundError(
                f"Unable to read image: {image_path}"
            )

        height, width = image.shape[:2]
        logger.debug("Original image dimensions: %dx%d", width, height)

        # -------------------------
        # Preprocessing Steps
        # -------------------------

        processed = image

        if self.config.use_grayscale:
            logger.info("Converting image to grayscale")
            processed = cv2.cvtColor(
                processed,
                cv2.COLOR_BGR2GRAY,
            )

        if self.config.use_blur:
            logger.info("Applying Gaussian blur (kernel size: %d)", self.config.blur_kernel_size)
            processed = cv2.GaussianBlur(
                processed,
                (
                    self.config.blur_kernel_size,
                    self.config.blur_kernel_size,
                ),
                0,
            )

        if self.config.use_threshold:
            logger.info(
                "Applying adaptive thresholding (block size: %d, constant: %d)",
                self.config.adaptive_block_size,
                self.config.adaptive_constant,
            )
            processed = cv2.adaptiveThreshold(
                processed,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                self.config.adaptive_block_size,
                self.config.adaptive_constant,
            )

        # -------------------------
        # Save processed image
        # -------------------------

        output_dir = "outputs/preprocessed"

        os.makedirs(
            output_dir,
            exist_ok=True,
        )

        filename = os.path.basename(image_path)

        output_path = os.path.join(
            output_dir,
            filename,
        )

        logger.info("Saving preprocessed image to: %s", output_path)
        cv2.imwrite(
            output_path,
            processed,
        )

        logger.info("Preprocessing complete for %s. Output path: %s", image_path, output_path)

        return ProcessedImage(
            original_path=image_path,
            processed_path=output_path,
            width=width,
            height=height,
        )