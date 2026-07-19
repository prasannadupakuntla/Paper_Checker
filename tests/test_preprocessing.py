import os
from pathlib import Path
import cv2
import numpy as np
import pytest

from backend.services.preprocessing.image_processor import ImagePreprocessor
from backend.services.preprocessing.validator import ImageValidator
from backend.services.preprocessing.exceptions import (
    ImageNotFoundError,
    UnsupportedImageFormatError,
    CorruptedImageError,
    ImageResolutionError,
)


def test_valid_image():
    """Test validating and preprocessing a valid image."""
    validator = ImageValidator()
    processor = ImagePreprocessor()
    
    image_path = "tests/handwritten.jpeg"
    
    # Assert validation passes
    assert validator.validate(image_path) is True
    
    # Assert preprocessing works
    result = processor.process(image_path)
    assert result.original_path == image_path
    assert Path(result.processed_path).exists()
    assert result.width > 0
    assert result.height > 0


def test_missing_image():
    """Test that validating or processing a non-existent image raises ImageNotFoundError."""
    validator = ImageValidator()
    processor = ImagePreprocessor()
    
    non_existent_path = "tests/does_not_exist.jpg"
    
    with pytest.raises(ImageNotFoundError):
        validator.validate(non_existent_path)
        
    with pytest.raises(ImageNotFoundError):
        processor.process(non_existent_path)


def test_unsupported_format(tmp_path):
    """Test that validating or processing an unsupported image format raises UnsupportedImageFormatError."""
    validator = ImageValidator()
    processor = ImagePreprocessor()
    
    # Create a temporary file with unsupported suffix (.txt)
    unsupported_file = tmp_path / "test.txt"
    unsupported_file.write_text("dummy text content")
    
    unsupported_path = str(unsupported_file)
    
    with pytest.raises(UnsupportedImageFormatError):
        validator.validate(unsupported_path)
        
    with pytest.raises(UnsupportedImageFormatError):
        processor.process(unsupported_path)


def test_corrupted_image(tmp_path):
    """Test that validating or processing a corrupted/unreadable image raises CorruptedImageError."""
    validator = ImageValidator()
    processor = ImagePreprocessor()
    
    # Create a temporary file with a supported suffix (.jpg) but corrupted bytes
    corrupted_file = tmp_path / "corrupted.jpg"
    corrupted_file.write_bytes(b"invalid image data header")
    
    corrupted_path = str(corrupted_file)
    
    with pytest.raises(CorruptedImageError):
        validator.validate(corrupted_path)
        
    with pytest.raises(CorruptedImageError):
        processor.process(corrupted_path)


def test_low_resolution_image(tmp_path):
    """Test that validating or processing an image below minimum resolution raises ImageResolutionError."""
    validator = ImageValidator()
    processor = ImagePreprocessor()
    
    # Create a tiny 100x100 black image
    low_res_img = np.zeros((100, 100, 3), dtype=np.uint8)
    low_res_file = tmp_path / "low_res.jpg"
    cv2.imwrite(str(low_res_file), low_res_img)
    
    low_res_path = str(low_res_file)
    
    with pytest.raises(ImageResolutionError):
        validator.validate(low_res_path)
        
    with pytest.raises(ImageResolutionError):
        processor.process(low_res_path)