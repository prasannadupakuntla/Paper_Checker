# 🧠 Keyword RAG Service

The **RAG (Retrieval-Augmented Generation) Service** connects raw student answers to specific curriculum modules, standardizing terminology tags for syllabus-aligned report generation.

---

## 🔍 Concept Matching

The service performs keyword-level lookup across a curriculum concept database:
* Matches terms like `glucose`, `co2`, `h2o` to `Chemical Equation`.
* Matches `light` / `dark` to `Light/Dark Reactions`.
* Maps unmatched texts to a general category (`General Biology Concepts`).

---

## 📁 File Structure

* **`interface.py`**: Defines the `RAGService` retrieval contract.
* **`service.py`**: Implements `KeywordRAGService` with predefined curriculum categories.

---

## 🚀 Usage Example

```python
from backend.services.rag.service import KeywordRAGService

rag_service = KeywordRAGService()

# Retrieve matching concepts
concepts = rag_service.retrieve_concepts("Plants absorb CO2 and release O2.")
print(f"Matched Curriculum Nodes: {concepts}")
# Outputs: Chemical Equation, Photosynthesis Definition
```
