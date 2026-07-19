# 🛡️ Confidence Engine Service

The **Confidence Service** calculates overall confidence metrics for OCR extraction and binarization quality. This ensures that educators can review "low confidence" student sheets manually.

---

## 📊 Confidence Calculation

The service evaluates:
* **Average OCR Character Confidence**: Baseline reliability score (0-100%).
* **Fallback Mechanisms**: Automatically assigns a default baseline if OCR confidence metadata is absent or empty (e.g., when mock OCR results are used during testing).

---

## 📁 File Structure

* **`interface.py`**: Defines the `ConfidenceService` contract.
* **`service.py`**: Implements `TextConfidenceService` to compute percentage values.

---

## 🚀 Usage Example

```python
from backend.services.confidence.service import TextConfidenceService
from backend.services.ocr.ocr_models import OCRResult

confidence_service = TextConfidenceService()

# Evaluate confidence from OCR result object
ocr_res = OCRResult(text="Hello", lines=[], average_confidence=0.89)
score = confidence_service.calculate_confidence(ocr_res)

print(f"Calculated OCR Trust Score: {score}%")  # Outputs: 89.0%
```
