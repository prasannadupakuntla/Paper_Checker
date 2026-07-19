import logging
from pathlib import Path

import cv2

from .exceptions import (
    CorruptedImageError,
    ImageNotFoundError,
    ImageResolutionError,
    UnsupportedImageFormatError,
)

logger = logging.getLogger(__name__)


class ImageValidator:
    """
    Validates images before preprocessing and OCR.
    """

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    MIN_WIDTH = 500
    MIN_HEIGHT = 500

    def validate(self, image_path: str) -> bool:
        """
        Validate an image before OCR.

        Args:
            image_path: Path to the image.

        Returns:
            True if validation succeeds.

        Raises:
            ImageNotFoundError
            UnsupportedImageFormatError
            CorruptedImageError
            ImageResolutionError
        """

        logger.info("Validating image: %s", image_path)
        path = Path(image_path)

        # File exists
        if not path.exists():
            logger.error("Image file not found: %s", image_path)
            raise ImageNotFoundError(
                f"Image not found: {image_path}"
            )

        # File extension
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            logger.error("Unsupported image format: %s for file %s", path.suffix, image_path)
            raise UnsupportedImageFormatError(
                f"Unsupported image format: {path.suffix}"
            )

        # Read image
        logger.debug("Reading image: %s", image_path)
        image = cv2.imread(str(path))

        if image is None:
            logger.error("Unable to read image (corrupted or unreadable): %s", image_path)
            raise CorruptedImageError(
                f"Unable to read image: {image_path}"
            )

        height, width = image.shape[:2]
        logger.debug("Image dimensions: %dx%d", width, height)

        # Resolution check
        if width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
            logger.error(
                "Image resolution too low (%dx%d). Minimum required: %dx%d",
                width,
                height,
                self.MIN_WIDTH,
                self.MIN_HEIGHT,
            )
            raise ImageResolutionError(
                f"Image resolution too low ({width}x{height}). "
                f"Minimum required: "
                f"{self.MIN_WIDTH}x{self.MIN_HEIGHT}"
            )

        logger.info("Image validation successful for %s", image_path)
        return True