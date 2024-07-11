from pydantic import BaseModel
from typing import List


class GameHistoryResponse(BaseModel):
    id: int
    user_id: int
    ai_personality_id: int
    start_time: str
    end_time: str | None
