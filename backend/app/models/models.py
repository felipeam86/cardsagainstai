from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base

# Association tables
card_set_black_card = Table(
    "card_set_black_card",
    Base.metadata,
    Column("card_set_id", Integer, ForeignKey("card_set.id"), primary_key=True),
    Column("black_card_id", Integer, ForeignKey("black_cards.id"), primary_key=True),
)

card_set_white_card = Table(
    "card_set_white_card",
    Base.metadata,
    Column("card_set_id", Integer, ForeignKey("card_set.id"), primary_key=True),
    Column("white_card_id", Integer, ForeignKey("white_cards.id"), primary_key=True),
)


class BlackCard(Base):
    __tablename__ = "black_cards"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    pick = Column(Integer, nullable=False)
    watermark = Column(String)

    card_sets = relationship(
        "CardSet", secondary=card_set_black_card, back_populates="black_cards"
    )


class WhiteCard(Base):
    __tablename__ = "white_cards"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    watermark = Column(String)

    card_sets = relationship(
        "CardSet", secondary=card_set_white_card, back_populates="white_cards"
    )


class CardSet(Base):
    __tablename__ = "card_set"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    black_cards = relationship(
        "BlackCard", secondary=card_set_black_card, back_populates="card_sets"
    )
    white_cards = relationship(
        "WhiteCard", secondary=card_set_white_card, back_populates="card_sets"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())

    game_sessions = relationship("GameSession", back_populates="user")
    ai_personalities = relationship("AIPersonality", back_populates="created_by")


class AIPersonality(Base):
    __tablename__ = "ai_personalities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="ai_personalities")
    game_sessions = relationship("GameSession", back_populates="ai_personality")


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ai_personality_id = Column(
        Integer, ForeignKey("ai_personalities.id"), nullable=False
    )
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime)

    user = relationship("User", back_populates="game_sessions")
    ai_personality = relationship("AIPersonality", back_populates="game_sessions")
    game_rounds = relationship("GameRound", back_populates="game_session")


class GameRound(Base):
    __tablename__ = "game_rounds"

    id = Column(Integer, primary_key=True)
    game_session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    round_number = Column(Integer, nullable=False)
    black_card_id = Column(Integer, ForeignKey("black_cards.id"), nullable=False)
    user_score = Column(Integer, nullable=False)
    ai_score = Column(Integer, nullable=False)
    winner = Column(String, nullable=False)
    judge_explanation = Column(String)

    game_session = relationship("GameSession", back_populates="game_rounds")
    black_card = relationship("BlackCard")
    card_plays = relationship("CardPlay", back_populates="game_round")


class CardPlay(Base):
    __tablename__ = "card_plays"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer, ForeignKey("game_rounds.id"), nullable=False)
    user_card_id = Column(Integer, ForeignKey("white_cards.id"), nullable=False)
    ai_card_id = Column(Integer, ForeignKey("white_cards.id"), nullable=False)
    play_order = Column(Integer, nullable=False)

    game_round = relationship("GameRound", back_populates="card_plays")
    user_card = relationship("WhiteCard", foreign_keys=[user_card_id])
    ai_card = relationship("WhiteCard", foreign_keys=[ai_card_id])
