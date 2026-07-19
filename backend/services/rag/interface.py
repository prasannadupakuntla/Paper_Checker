from abc import ABC, abstractmethod

class RAGService(ABC):
    @abstractmethod
    def retrieve_concepts(self, text: str) -> str:
        """
        Query a concept store or reference materials using the text
        and return retrieved concepts as a formatted string.
        """
        pass
