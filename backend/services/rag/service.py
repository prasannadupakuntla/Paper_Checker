import logging
from .interface import RAGService

logger = logging.getLogger(__name__)

class KeywordRAGService(RAGService):
    """
    RAG-style concept retriever matching OCR text to a predefined library of curriculum concepts.
    """
    def __init__(self, concepts_db: dict = None):
        # A simple knowledge database mapping key terms to standard curriculum concepts
        self.concepts_db = concepts_db or {
            "photosynthesis": "Photosynthesis Definition",
            "process": "Photosynthesis Definition",
            "plants": "Photosynthesis Definition",
            "light": "Light/Dark Reactions",
            "dark": "Light/Dark Reactions",
            "reaction": "Light/Dark Reactions",
            "co2": "Chemical Equation",
            "h2o": "Chemical Equation",
            "glucose": "Chemical Equation",
            "oxygen": "Chemical Equation",
            "equation": "Chemical Equation",
        }

    def retrieve_concepts(self, text: str) -> str:
        logger.info("Retrieving relevant curriculum concepts via RAG...")
        lower_text = text.lower()
        matched = set()
        
        for key, concept in self.concepts_db.items():
            if key in lower_text:
                matched.add(concept)
                
        if not matched:
            return "General Biology Concepts"
            
        retrieved = ", ".join(sorted(matched))
        logger.info("Retrieved concepts: %s", retrieved)
        return retrieved
