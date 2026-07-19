from __future__ import annotations
import re
import difflib
import logging
from collections import defaultdict
from backend.services.ocr.ocr_models import OCRResult

logger = logging.getLogger(__name__)

class ConfusionMiner:
    """
    Compares OCR outputs with expected references using word and character sequence alignment
    to extract character confusion mappings.
    """
    @staticmethod
    def mine_confusions(ocr_result: OCRResult, reference_text: str) -> dict[str, str]:
        # Clean text helper to extract alphanumeric words
        def clean_to_words(text):
            cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
            return [w for w in cleaned.split() if w]

        expected_words = clean_to_words(reference_text)
        ocr_words = clean_to_words(ocr_result.text)

        sub_counts = defaultdict(lambda: defaultdict(int))

        # Align expected reference words with raw OCR words
        matcher = difflib.SequenceMatcher(None, expected_words, ocr_words)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                len_exp = i2 - i1
                len_ocr = j2 - j1
                for k in range(min(len_exp, len_ocr)):
                    exp_word = expected_words[i1 + k].lower()
                    ocr_word = ocr_words[j1 + k].lower()

                    # Align characters within the words
                    char_matcher = difflib.SequenceMatcher(None, exp_word, ocr_word)
                    for c_tag, ci1, ci2, cj1, cj2 in char_matcher.get_opcodes():
                        if c_tag == 'replace':
                            # Single character substitution detection
                            if ci2 - ci1 == 1 and cj2 - cj1 == 1:
                                exp_char = exp_word[ci1]
                                ocr_char = ocr_word[cj1]
                                if exp_char != ocr_char:
                                    sub_counts[ocr_char][exp_char] += 1

        common_confusions = {}
        for ocr_char, targets in sub_counts.items():
            best_target = max(targets, key=targets.get)
            common_confusions[ocr_char] = best_target
            logger.info("Modular Confusion Miner: Mapped '%s' ➔ '%s' (count: %d)", ocr_char, best_target, targets[best_target])

        return common_confusions
