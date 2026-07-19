from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict

class PhysicalMetrics(BaseModel):
    average_height: float = 0.0
    average_width: float = 0.0
    word_spacing: float = 0.0
    line_spacing: float = 0.0
    slant: float = 0.0

class HandwritingProfile(BaseModel):
    student_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    physical_metrics: PhysicalMetrics
    common_confusions: Dict[str, str] = Field(default_factory=dict)
