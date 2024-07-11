from datetime import datetime
from pydantic import BaseModel


class AIPersonalityInput(BaseModel):
    name: str
    description: str


class AIPersonalityResponse(AIPersonalityInput):
    id: int
    name: str
    description: str
    created_at: datetime
    created_by: int
