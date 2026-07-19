from pydantic import BaseModel


class ProcessedImage(BaseModel):
    original_path: str
    processed_path: str
    width: int
    height: int