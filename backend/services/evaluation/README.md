# 📝 Rubric Evaluation Service

The **Evaluation Service** grades corrected student answer text against pre-defined rubrics. It automatically analyzes answer matches, scores each segment, compiles a detailed breakdown, and provides actionable student feedback.

---

## ⚙️ Grading Logic & Rubric Matching

The service parses student text to match key grading criteria:
* **Definition Matching**: Scans for definitions and terminology.
* **Concept Check**: Assesses depth of explanations (e.g., matching light/dark reactions).
* **Formula & Equations**: Searches for correct chemical or mathematical expressions.

### Score Calculation Flow
```
[Corrected Student Text]
           │
           ▼
  [Check Key terms]
  ├── "photosynthesis" / "process" ──► Definition Score (+3.5 marks)
  ├── "light" / "dark" / "reaction" ──► Reactions Score (+3.0 marks)
  └── "co2" / "h2o" / "glucose" ──────► Equation Score (+2.0 marks)
           │
           ▼
[Feedback & Deficit Report] ◄────── If score < 10.0
```

---

## 📁 File Structure

* **`interface.py`**: Defines the `EvaluationService` interface contract.
* **`service.py`**: Implements the `RubricEvaluationService` containing standard Photosynthesis rubric checking and feedback compilation.

---

## 🚀 Usage Example

```python
from backend.services.evaluation.service import RubricEvaluationService

# Initialize evaluator with optional custom rubric
evaluator = RubricEvaluationService()

student_answer = "Photosynthesis is the process in plants. It has light and dark reactions. Equation is 6CO2 + 6H2O."
result = evaluator.evaluate_answer(student_answer)

print(f"Final Score: {result['score']}/10.0")
print(f"Feedback:\n{result['feedback']}")
```

> [!TIP]
> The evaluation service is modularized to support injecting custom rubric rules in future enhancements.
