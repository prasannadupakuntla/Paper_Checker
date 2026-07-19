from __future__ import annotations
import re
import logging
from statistics import mean
from backend.services.ocr.ocr_models import OCRResult, OCRLine
from .calibration_models import HandwritingProfile

logger = logging.getLogger(__name__)

class TextCorrector:
    """
    Applies handwriting confusion mapping to correct raw OCR tokens and adjust confidence values.
    """
    def __init__(self, dictionary: set[str]):
        self.dictionary = dictionary

    def correct_word(self, word: str, confusions: dict[str, str]) -> str:
        """
        Attempts to correct a single word based on the confusion mapping.
        Generates combinations of substitutions to find a valid dictionary word.
        Preserves original capitalization and surrounding punctuation.
        """
        match = re.match(r'^([^a-zA-Z0-9]*)(.*?)([^a-zA-Z0-9]*)$', word)
        if not match:
            return word

        prefix, core, suffix = match.groups()
        if not core:
            return word

        core_lower = core.lower()
        if core_lower in self.dictionary:
            return word

        # Find all positions where characters have confusion mappings
        mutable_positions = [i for i, c in enumerate(core_lower) if c in confusions]
        if not mutable_positions:
            return word

        # Limit to 8 mutable positions to avoid exponential complexity (2^8 = 256)
        n = min(len(mutable_positions), 8)
        mutable_positions = mutable_positions[:n]

        # Generate combinations of substitutions (from least changes to most changes)
        # We sort by the number of substitutions made (Hamming weight of mask)
        masks = range(1, 1 << n)
        sorted_masks = sorted(masks, key=lambda m: bin(m).count('1'))

        corrected_core = None
        for mask in sorted_masks:
            chars = list(core_lower)
            for k in range(n):
                if (mask >> k) & 1:
                    pos = mutable_positions[k]
                    orig_char = chars[pos]
                    chars[pos] = confusions[orig_char]
            
            candidate = "".join(chars)
            if candidate in self.dictionary:
                corrected_core = candidate
                break

        if corrected_core:
            # Preserve original casing
            if core.isupper():
                core_corrected = corrected_core.upper()
            elif core[0].isupper():
                core_corrected = corrected_core.capitalize()
            else:
                core_corrected = corrected_core

            logger.info("Modular Corrector: Corrected '%s' ➔ '%s'", core, core_corrected)
            return f"{prefix}{core_corrected}{suffix}"

        return word

    def correct_ocr_result(self, ocr_result: OCRResult, profile: HandwritingProfile) -> OCRResult:
        """
        Applies a student's handwriting profile to correct character substitution errors
        and adjust the line/result confidence metrics.
        """
        if not profile.common_confusions:
            return ocr_result

        corrected_lines: list[OCRLine] = []
        confidences = []

        for line in ocr_result.lines:
            words = line.text.split(" ")
            corrected_words = [self.correct_word(w, profile.common_confusions) for w in words]
            corrected_text = " ".join(corrected_words)

            confidence = line.confidence
            if corrected_text != line.text:
                confidence = min(0.98, max(confidence + 0.15, 0.90))

            confidences.append(confidence)
            corrected_lines.append(
                OCRLine(
                    text=corrected_text,
                    confidence=round(confidence, 3),
                    box=line.box
                )
            )

        full_text = "\n".join(line.text for line in corrected_lines)
        avg_confidence = mean(confidences) if confidences else 0.0

        return OCRResult(
            text=full_text,
            lines=corrected_lines,
            average_confidence=round(avg_confidence, 3)
        )
