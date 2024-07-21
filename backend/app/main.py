from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from app.db.database import get_session
from app.db.models import AIPersonality, BlackCard, GameSession, GameRound, WhiteCard
from app.services.game import GameService
from app.services.card_manager import CardManagerService
from app.services.anthropic import AnthropicService
from pydantic import BaseModel

app = FastAPI()


def get_game_service(db: Session = Depends(get_session)):
    card_manager = CardManagerService(db)
    anthropic_service = AnthropicService()
    return GameService(db, anthropic_service, card_manager)


class AIPersonalityCreate(BaseModel):
    name: str
    description: str


class GameSessionCreate(BaseModel):
    username: str
    ai_personality_id: int


class GameRoundCreate(BaseModel):
    game_session_id: int


class GameRoundResponse(BaseModel):
    game_round: GameRound
    black_card: BlackCard
    white_cards: List[WhiteCard]


class GameRoundResult(BaseModel):
    game_round: GameRound
    ai_chosen_cards: List[WhiteCard]


class CardSubmission(BaseModel):
    user_card_ids: List[int]
    white_card_ids: List[int]


class GameResult(BaseModel):
    game_session_id: int
    user_score: int
    ai_score: int
    winner: str
    rounds_played: int


@app.get("/ai-personalities", response_model=List[AIPersonality])
def get_ai_personalities(db: Session = Depends(get_session)):
    personalities = db.exec(select(AIPersonality)).all()
    return personalities


@app.post("/ai-personalities", response_model=AIPersonality, status_code=201)
def create_ai_personality(
    personality: AIPersonalityCreate, db: Session = Depends(get_session)
):
    db_personality = AIPersonality(
        name=personality.name, description=personality.description
    )
    db.add(db_personality)
    db.commit()
    db.refresh(db_personality)
    return db_personality


@app.post("/game-sessions", response_model=GameSession, status_code=201)
async def create_game_session(
    session_data: GameSessionCreate,
    game_service: GameService = Depends(get_game_service),
):
    try:
        game_session = await game_service.create_game_session(
            session_data.username, session_data.ai_personality_id
        )
        return game_session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/game-sessions/{session_id}/end", response_model=GameResult)
async def end_game_session(
    session_id: int, game_service: GameService = Depends(get_game_service)
):
    try:
        result = game_service.end_game_session(session_id)
        return GameResult(
            game_session_id=result["game_session_id"],
            user_score=result["user_score"],
            ai_score=result["ai_score"],
            winner=result["winner"],
            rounds_played=result["rounds_played"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/game-rounds", response_model=GameRoundResponse)
async def create_game_round(
    round_data: GameRoundCreate, game_service: GameService = Depends(get_game_service)
):
    try:
        game_round, black_card, white_cards = await game_service.create_game_round(
            round_data.game_session_id
        )
        return GameRoundResponse(
            game_round=game_round,
            black_card=black_card,
            white_cards=white_cards,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/game-rounds/{round_id}/submit", response_model=GameRoundResult)
async def submit_game_round(
    round_id: int,
    submission: CardSubmission,
    game_service: GameService = Depends(get_game_service),
):
    try:
        game_round, ai_chosen_cards = await game_service.submit_game_round(
            round_id, submission.user_card_ids, submission.white_card_ids
        )
        return GameRoundResult(
            game_round=game_round,
            ai_chosen_cards=ai_chosen_cards,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
