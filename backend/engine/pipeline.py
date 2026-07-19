import os
import logging
from backend.services.preprocessing.image_processor import ImagePreprocessor
from backend.services.ocr.paddle_service import PaddleOCRService
from backend.services.calibration.service import FileCalibrationService
from backend.services.evaluation.service import RubricEvaluationService
from backend.services.confidence.service import TextConfidenceService
from backend.services.rag.service import KeywordRAGService

logger = logging.getLogger(__name__)

class EvaluationPipeline:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.ocr_service = PaddleOCRService()
        self.calibration_service = FileCalibrationService()
        self.evaluation_service = RubricEvaluationService()
        self.confidence_service = TextConfidenceService()
        self.rag_service = KeywordRAGService()

    def run(self, image_id: str, student_id: str = None, uploads_dir: str = "backend/uploads") -> dict:
        # 1. Find the image file
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir, exist_ok=True)
            
        matching_files = [f for f in os.listdir(uploads_dir) if f.startswith(image_id)]
        if not matching_files:
            raise FileNotFoundError(f"Image with ID {image_id} not found.")
        
        image_path = os.path.join(uploads_dir, matching_files[0])
        
        # 2. Preprocess the image
        logger.info("Pipeline: Preprocessing image...")
        processed_image = self.preprocessor.process(image_path)
        
        # 3. Run OCR
        logger.info("Pipeline: Running OCR...")
        ocr_result = self.ocr_service.extract_text(processed_image.processed_path)
        
        # 4. Calibration (Perspective correction & text cleanup)
        logger.info("Pipeline: Running Calibration...")
        if student_id:
            profile = self.calibration_service.load_profile(student_id)
            if profile:
                logger.info("Pipeline: Found handwriting profile for student %s. Applying calibration...", student_id)
                ocr_result = self.calibration_service.correct_ocr_result(ocr_result, profile)
            else:
                logger.warning("Pipeline: Profile for student %s not found. Proceeding with raw OCR.", student_id)
        else:
            logger.info("Pipeline: No student_id provided. Skipping calibration.")

        corrected_ocr = ocr_result.text.strip()
        if not corrected_ocr:
            corrected_ocr = "No text detected in the image."
        
        # 5. Evaluation & Rubric Matching
        logger.info("Pipeline: Running Evaluation...")
        eval_result = self.evaluation_service.evaluate_answer(corrected_ocr)
        
        # 6. Confidence Engine
        confidence = self.confidence_service.calculate_confidence(ocr_result)
            
        # 7. Concept Retrieval (RAG)
        retrieved_concept = self.rag_service.retrieve_concepts(corrected_ocr)
        
        # original_image_url will be served by the static files handler in FastAPI
        original_image_url = f"/uploads/{os.path.basename(image_path)}"
        
        return {
            "image_id": image_id,
            "original_image_url": original_image_url,
            "ocr_text": ocr_result.text,
            "corrected_ocr": corrected_ocr,
            "retrieved_concept": retrieved_concept,
            "rubric": eval_result["rubric"],
            "evaluation": eval_result["evaluation"],
            "confidence": confidence,
            "feedback": eval_result["feedback"]
        }
