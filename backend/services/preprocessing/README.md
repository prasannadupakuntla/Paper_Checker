# 📷 Image Preprocessing Service

The **Preprocessing Service** cleans, adjusts, and normalizes raw student answer sheets before passing them to the OCR engine. This step is critical to reducing OCR failures caused by poor lighting, tilted papers, or page noise.

---

## 🛠️ Preprocessing Pipeline

When an image path is passed to the preprocessor, it executes the following sequence:

```mermaid
graph LR
    A[Raw Image File] --> B[Validation & Loading]
    B --> C[Grayscale Conversion]
    C --> D[Adaptive Thresholding]
    D --> E[Skew Detection & Rotation]
    E --> F[Size Normalization]
    F --> G[Save Preprocessed Image]
```

1. **Validation**: Confirms file size (under limit), MIME type, and dimensions.
2. **Grayscale Conversion**: Reduces dimensional complexity for thresholding.
3. **Binarization (Adaptive Thresholding)**: Converts the image to black-and-white to isolate ink strokes from page background noise and shadow gradients.
4. **Skew/Rotation Alignment**: Detects text orientation angles and rotates the image to ensure lines are horizontally aligned.
5. **Normalization**: Resizes the image within optimal boundaries for fast OCR parsing.

---

## 📁 File Structure

* **`interface.py`**: Declares the abstract `ImagePreprocessorInterface` contract.
* **`image_processor.py`**: The core implementation (`ImagePreprocessor`) utilizing OpenCV.
* **`validator.py`**: Implements basic validation logic for dimensions and formats.
* **`image_models.py`**: Pydantic schemas for preprocessing input/output parameters.
* **`exceptions.py`**: Module-specific exception handlers.
* **`config.py`**: Configurable settings (e.g., maximum file sizes, supported types, target widths).

---

## 🚀 Usage Example

```python
from backend.services.preprocessing.image_processor import ImagePreprocessor

# Initialize preprocessor
preprocessor = ImagePreprocessor()

# Process an image file
result = preprocessor.process("backend/uploads/my_paper.jpg")

print(f"Processed path: {result.processed_path}")
print(f"Is preprocessed: {result.is_preprocessed}")
print(f"Original shape: {result.original_shape}")
```

> [!IMPORTANT]
> Always verify that your uploaded files conform to the standard formats (JPEG, PNG, PDF) and do not exceed the size limit configured in `config.py` (default: 10MB).
