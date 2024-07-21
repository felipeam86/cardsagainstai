from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


def utc_now():
    return datetime.now(timezone.utc)


class BlackCard(SQLModel, table=True):
    __tablename__ = "black_cards"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    pick: int
    watermark: Optional[str] = None
    category: Optional[str] = None


class WhiteCard(SQLModel, table=True):
    __tablename__ = "white_cards"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    watermark: Optional[str] = None
    category: Optional[str] = None


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    created_at: datetime = Field(default_factory=utc_now)


class AIPersonality(SQLModel, table=True):
    __tablename__ = "ai_personalities"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")


class GameSession(SQLModel, table=True):
    __tablename__ = "game_sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    ai_personality_id: int = Field(foreign_key="ai_personalities.id")
    start_time: datetime = Field(default_factory=utc_now)
    end_time: Optional[datetime] = None


class GameRound(SQLModel, table=True):
    __tablename__ = "game_rounds"

    id: Optional[int] = Field(default=None, primary_key=True)
    game_session_id: int = Field(foreign_key="game_sessions.id")
    round_number: int
    black_card_id: int = Field(foreign_key="black_cards.id")
    user_score: int
    ai_score: int
    winner: str
    judge_explanation: Optional[str] = None


class CardPlay(SQLModel, table=True):
    __tablename__ = "card_plays"

    id: Optional[int] = Field(default=None, primary_key=True)
    round_id: int = Field(foreign_key="game_rounds.id")
    user_card_id: int = Field(foreign_key="white_cards.id")
    ai_card_id: int = Field(foreign_key="white_cards.id")
    play_order: int
