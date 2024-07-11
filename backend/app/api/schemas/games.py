from datetime import datetime
from pydantic import BaseModel
from typing import List


class GameSessionResponse(BaseModel):
    id: int
    user_id: int
    ai_personality_id: int
    start_time: datetime
    end_time: datetime | None


class GameSessionCreate(BaseModel):
    user_id: int
    ai_personality_id: int


class GameRoundResponse(BaseModel):
    id: int
    game_session_id: int
    round_number: int
    black_card_id: int
    user_score: int
    ai_score: int
    winner: str
    judge_explanation: str


class CardPlay(BaseModel):
    id: int
    round_id: int
    user_card_id: int
    ai_card_id: int
    play_order: int


class CardSubmission(BaseModel):
    user_card_ids: List[int]
    ai_card_ids: List[int]


class GameStateResponse(BaseModel):
    available_slots: int
    max_users: int
