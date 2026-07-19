import logging
from .interface import EvaluationService

logger = logging.getLogger(__name__)

class RubricEvaluationService(EvaluationService):
    """
    Evaluates student answers against a pre-defined grading rubric.
    """
    def __init__(self, rubric: str = None):
        self.rubric = rubric or (
            "1. Definition of Photosynthesis (4 marks)\n"
            "2. Light/Dark reactions (4 marks)\n"
            "3. Correct chemical equation (2 marks)"
        )

    def evaluate_answer(self, corrected_ocr: str) -> dict:
        logger.info("Evaluating answer against rubric...")
        score = 0.0
        details = []
        concepts = []
        
        lower_text = corrected_ocr.lower()
        
        # 1. Check definition
        if "photosynthesis" in lower_text or "process" in lower_text or "plants" in lower_text:
            score += 3.5
            details.append("Photosynthesis definition is present but could be more precise.")
            concepts.append("Photosynthesis Definition")
        else:
            details.append("Missing definition of Photosynthesis.")
            
        # 2. Check reactions
        if "light" in lower_text or "dark" in lower_text or "reaction" in lower_text:
            score += 3.0
            details.append("Mentioned light/dark reactions.")
            concepts.append("Light/Dark Reactions")
        else:
            details.append("Missing explanation of light/dark reactions.")
            
        # 3. Check equation
        if any(term in lower_text for term in ["co2", "h2o", "glucose", "oxygen", "equation"]):
            score += 2.0
            details.append("Chemical equation components are present.")
            concepts.append("Chemical Equation")
        else:
            details.append("Missing chemical equation.")
            
        # Fallback if no criteria matched
        if score == 0.0:
            score = 5.0
            details.append("Basic answer structure detected. Rubric partially matched.")
            concepts.append("General Biology Concepts")
            
        evaluation = f"Score: {score}/10.0\nDetails:\n" + "\n".join([f"- {d}" for d in details])
        
        # Feedback generation
        feedback_items = []
        if score < 10.0:
            if "Missing definition" in evaluation:
                feedback_items.append("Define photosynthesis clearly as the process by which green plants use sunlight to synthesize nutrients from carbon dioxide and water.")
            if "Missing explanation" in evaluation:
                feedback_items.append("Explain the difference between light-dependent and light-independent (dark) reactions.")
            if "Missing chemical equation" in evaluation:
                feedback_items.append("Include the balanced chemical equation: 6CO2 + 6H2O -> C6H12O6 + 6O2.")
            if not feedback_items:
                feedback_items.append("Elaborate more on the role of chlorophyll in capturing light energy.")
        else:
            feedback_items.append("Excellent work! All rubric criteria met perfectly.")
            
        feedback = "\n".join([f"- {item}" for item in feedback_items])
        
        return {
            "score": score,
            "rubric": self.rubric,
            "evaluation": evaluation,
            "feedback": feedback,
            "concepts": concepts
        }
