class ImageValidationError(Exception):
    """Base exception for image validation errors."""
    pass


class ImageNotFoundError(ImageValidationError):
    """Raised when the image file does not exist."""
    pass


class UnsupportedImageFormatError(ImageValidationError):
    """Raised when the image format is not supported."""
    pass


class CorruptedImageError(ImageValidationError):
    """Raised when the image cannot be opened."""
    pass


class ImageResolutionError(ImageValidationError):
    """Raised when the image resolution is too low."""
    pass