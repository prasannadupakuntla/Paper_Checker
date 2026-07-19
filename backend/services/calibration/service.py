from __future__ import annotations

import os
import json
import logging

from backend.services.ocr.ocr_models import OCRResult
from .interface import CalibrationService
from .calibration_models import HandwritingProfile
from .config import PROFILES_DIR
from .metrics import PhysicalMetricsExtractor
from .alignment import ConfusionMiner
from .corrector import TextCorrector

logger = logging.getLogger(__name__)


class FileCalibrationService(CalibrationService):
    """
    File-based implementation of the CalibrationService, orchestrating submodules.
    
    Responsibilities:
        - Calibrate student's handwriting by coordinating submodules.
        - Save/load profiles as JSON files using modern Pydantic APIs.
    """

    def __init__(self, profiles_dir: str = PROFILES_DIR):
        self.profiles_dir = profiles_dir
        os.makedirs(self.profiles_dir, exist_ok=True)
        logger.info("Initialized Modular FileCalibrationService with profiles directory: %s", self.profiles_dir)

        # Base dictionary populated with general and subject-specific vocabulary
        self.dictionary = {
            # general english words
            "the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "a", "an", "and", "is", "are", 
            "was", "were", "of", "in", "on", "at", "to", "for", "with", "by", "about", "this", "that", "these",
            # biology / science words
            "photosynthesis", "process", "green", "plants", "use", "sunlight", "synthesize", "nutrients",
            "carbon", "dioxide", "water", "chloroplasts", "chlorophyll", "light", "dark", "reaction", 
            "reactions", "calvin", "cycle", "produce", "glucose", "chemical", "equation", "oxygen", "solar", "energy",
            # physics / electricity words
            "electricity", "electric", "current", "voltage", "resistance", "ohms", "law", "circuit", 
            "battery", "electron", "potential", "difference", "power", "conductors", "insulators", "charge",
            "series", "parallel", "resistor", "resistors"
        }
        self.corrector = TextCorrector(self.dictionary)

    def calibrate(self, student_id: str, ocr_result: OCRResult, reference_text: str) -> HandwritingProfile:
        logger.info("Modular Calibrator: Calibrating student ID %s", student_id)
        
        # Dynamically expand corrector vocabulary from calibration reference words
        for word in reference_text.split():
            clean_word = "".join(c for c in word.lower() if c.isalnum())
            if clean_word:
                self.dictionary.add(clean_word)
                self.corrector.dictionary.add(clean_word)

        # 1. Extract physical metrics from bounding boxes
        physical_metrics = PhysicalMetricsExtractor.extract(ocr_result)

        # 2. Mine common confusions via sequence alignment
        common_confusions = ConfusionMiner.mine_confusions(ocr_result, reference_text)

        profile = HandwritingProfile(
            student_id=student_id,
            physical_metrics=physical_metrics,
            common_confusions=common_confusions
        )

        return profile

    def correct_ocr_result(self, ocr_result: OCRResult, profile: HandwritingProfile) -> OCRResult:
        return self.corrector.correct_ocr_result(ocr_result, profile)

    def save_profile(self, profile: HandwritingProfile) -> None:
        """
        Saves a student's handwriting profile to a local JSON file using Pydantic V2 APIs.
        """
        file_path = os.path.join(self.profiles_dir, f"{profile.student_id}.json")
        try:
            with open(file_path, "w") as f:
                # Use model_dump_json for Pydantic V2 compatibility
                f.write(profile.model_dump_json(indent=4))
            logger.info("Saved modular handwriting profile for student %s to %s", profile.student_id, file_path)
        except Exception as e:
            logger.exception("Failed to save handwriting profile for student %s", profile.student_id)
            raise RuntimeError(f"Failed to save profile: {e}") from e

    def load_profile(self, student_id: str) -> HandwritingProfile | None:
        """
        Loads a student's handwriting profile from a local JSON file.
        """
        file_path = os.path.join(self.profiles_dir, f"{student_id}.json")
        if not os.path.exists(file_path):
            logger.warning("No handwriting profile found for student ID: %s", student_id)
            return None

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            profile = HandwritingProfile(**data)
            logger.info("Loaded modular handwriting profile for student %s", student_id)
            return profile
        except Exception as e:
            logger.exception("Failed to load handwriting profile for student %s", student_id)
            return None
