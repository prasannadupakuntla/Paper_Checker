import os
import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_upload_and_evaluate():
    # Ensure test file exists
    test_image_path = "tests/sample.jpeg"
    assert os.path.exists(test_image_path), "Sample image for testing not found."

    # 1. Test Upload
    with open(test_image_path, "rb") as img:
        response = client.post(
            "/upload",
            files={"file": ("sample.jpeg", img, "image/jpeg")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "image_id" in data
    image_id = data["image_id"]

    # 2. Test Evaluate
    response = client.post(
        "/evaluate",
        json={"image_id": image_id}
    )
    
    assert response.status_code == 200
    eval_data = response.json()
    assert eval_data["image_id"] == image_id
    assert "ocr_text" in eval_data
    assert "corrected_ocr" in eval_data
    assert "evaluation" in eval_data
    assert "confidence" in eval_data
    assert "feedback" in eval_data
    assert eval_data["confidence"] > 0
