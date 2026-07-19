from pydantic import BaseModel


class OCRLine(BaseModel):
    text: str
    confidence: float
    box: list


class OCRResult(BaseModel):
    text: str
    lines: list[OCRLine]
    average_confidence: float