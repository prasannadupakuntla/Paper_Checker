import os
import shutil
import pytest
from fastapi.testclient import TestClient
from backend.app import app
from backend.services.ocr.ocr_models import OCRResult, OCRLine
from backend.services.calibration.service import FileCalibrationService

client = TestClient(app)

def test_calibration_service_direct():
    service = FileCalibrationService(profiles_dir="backend/uploads/test_profiles")
    
    # Pre-configure simulated OCRResult for calibration sheet
    # Expected words: "Resistance is basic. Current is flow."
    # OCR words: "Reslstance is baslc. Currcnt is flow."
    ocr_result = OCRResult(
        text="Reslstance is baslc. Currcnt is flow.",
        lines=[
            OCRLine(
                text="Reslstance is baslc. Currcnt is flow.",
                confidence=0.75,
                box=[[10, 10], [200, 10], [200, 30], [10, 30]] # slant=0, height=20, width=190
            )
        ],
        average_confidence=0.75
    )
    
    reference_text = "Resistance is basic. Current is flow."
    
    # Run calibration
    profile = service.calibrate("test_student_123", ocr_result, reference_text)
    
    assert profile.student_id == "test_student_123"
    assert profile.physical_metrics.average_height == 20.0
    
    # Common confusions should map:
    # 'l' -> 'i' (from Reslstance -> Resistance, and baslc -> basic)
    # 'c' -> 'e' (from Currcnt -> Current)
    assert profile.common_confusions.get('l') == 'i'
    assert profile.common_confusions.get('c') == 'e'
    
    # Save profile
    service.save_profile(profile)
    assert os.path.exists("backend/uploads/test_profiles/test_student_123.json")
    
    # Load profile
    loaded = service.load_profile("test_student_123")
    assert loaded is not None
    assert loaded.student_id == "test_student_123"
    assert loaded.common_confusions.get('l') == 'i'
    
    # Correcting text
    test_ocr_exam = OCRResult(
        text="This circuit has low reslstance.",
        lines=[
            OCRLine(
                text="This circuit has low reslstance.",
                confidence=0.70,
                box=[[10, 10], [100, 10], [100, 30], [10, 30]]
            )
        ],
        average_confidence=0.70
    )
    
    corrected = service.correct_ocr_result(test_ocr_exam, loaded)
    assert "resistance" in corrected.text.lower()
    # Confidence should be boosted from 0.70
    assert corrected.average_confidence > 0.70
    
    # Clean up test profiles
    shutil.rmtree("backend/uploads/test_profiles", ignore_errors=True)

def test_api_calibration_flow():
    # 1. Upload calibration image
    test_image_path = "tests/sample.jpeg"
    assert os.path.exists(test_image_path)
    
    with open(test_image_path, "rb") as img:
        response = client.post(
            "/upload",
            files={"file": ("sample.jpeg", img, "image/jpeg")}
        )
    assert response.status_code == 200
    image_id = response.json()["image_id"]
    
    # 2. Calibrate API
    # We provide a reference text matching the mock output for standard flow
    reference_text = (
        "Photosynthesis is the process by which green plants use sunlight to synthesize nutrients "
        "from carbon dioxide and water. In plants, photosynthesis occurs in chloroplasts. "
        "Light reactions capture solar energy, while dark reactions (Calvin cycle) produce glucose. "
        "The chemical equation is: 6CO2 + 6H2O -> C6H12O6 + 6O2."
    )
    
    response = client.post(
        "/calibrate",
        json={
            "student_id": "api_test_student",
            "image_id": image_id,
            "reference_text": reference_text
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "api_test_student"
    assert "profile" in data
    
    # 3. Evaluate API with student_id
    response = client.post(
        "/evaluate",
        json={
            "image_id": image_id,
            "student_id": "api_test_student"
        }
    )
    assert response.status_code == 200
    eval_data = response.json()
    assert eval_data["image_id"] == image_id
    assert "corrected_ocr" in eval_data
    
    # Clean up calibrated profile
    profile_path = "backend/uploads/profiles/api_test_student.json"
    if os.path.exists(profile_path):
        os.remove(profile_path)
