from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class GameSessionCreate(BaseModel):
    user_id: int
    ai_personality_id: int


class GameSessionResponse(BaseModel):
    id: int
    user_id: int
    ai_personality_id: int
    start_time: datetime
    end_time: Optional[datetime]


class GameStateResponse(BaseModel):
    available_slots: int
    max_users: int


class CardSubmission(BaseModel):
    user_card_ids: List[int]
    ai_card_ids: List[int]


class GameRound(BaseModel):
    id: int
    game_session_id: int
    round_number: int
    black_card_id: int
    user_score: int
    ai_score: int
    winner: str
    judge_explanation: str
