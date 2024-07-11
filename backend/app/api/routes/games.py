from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.models import (
    GameSession,
    User,
    AIPersonality,
    GameRound,
    BlackCard,
    WhiteCard,
    CardPlay,
)
from ..schemas.games import (
    GameSessionResponse,
    GameSessionCreate,
    GameRoundResponse,
    CardSubmission,
    GameStateResponse,
)

from ...services.redis_service import RedisService
from typing import List

router = APIRouter()


@router.post("/game-sessions", response_model=GameSessionResponse)
async def create_game_session(game: GameSessionCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == game.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ai_personality = (
        db.query(AIPersonality)
        .filter(AIPersonality.id == game.ai_personality_id)
        .first()
    )
    if not ai_personality:
        raise HTTPException(status_code=404, detail="AI Personality not found")

    new_game = GameSession(
        user_id=game.user_id, ai_personality_id=game.ai_personality_id
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    await RedisService.set_game_state(
        str(new_game.id),
        {"status": "created", "current_round": 0, "user_score": 0, "ai_score": 0},
    )

    return GameSessionResponse(
        id=new_game.id,
        user_id=new_game.user_id,
        ai_personality_id=new_game.ai_personality_id,
        start_time=str(new_game.start_time),
        end_time=str(new_game.end_time) if new_game.end_time else None,
    )


@router.get("/game-sessions/{session_id}", response_model=GameSessionResponse)
async def get_game_session(session_id: int, db: Session = Depends(get_db)):
    game = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game session not found")

    return GameSessionResponse(
        id=game.id,
        user_id=game.user_id,
        ai_personality_id=game.ai_personality_id,
        start_time=str(game.start_time),
        end_time=str(game.end_time) if game.end_time else None,
    )


@router.post("/game-sessions/{session_id}/start")
async def start_game_session(session_id: int, db: Session = Depends(get_db)):
    game = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game session not found")

    game_state = await RedisService.get_game_state(str(session_id))
    if game_state["status"] != "created":
        raise HTTPException(status_code=400, detail="Game already started")

    await RedisService.set_game_state(
        str(session_id),
        {"status": "in_progress", "current_round": 1, "user_score": 0, "ai_score": 0},
    )

    return {"detail": "Game session started"}


@router.post("/game-rounds/{round_id}/submit")
async def submit_card_plays(
    round_id: int, submission: CardSubmission, db: Session = Depends(get_db)
):
    game_round = db.query(GameRound).filter(GameRound.id == round_id).first()
    if not game_round:
        raise HTTPException(status_code=404, detail="Game round not found")

    # Implement card submission logic here

    return {"detail": "Cards submitted"}


@router.get("/game-rounds/{round_id}/result", response_model=GameRound)
async def get_round_result(round_id: int, db: Session = Depends(get_db)):
    game_round = db.query(GameRound).filter(GameRound.id == round_id).first()
    if not game_round:
        raise HTTPException(status_code=404, detail="Game round not found")

    # Implement round result logic here

    return {"detail": "Round result"}


@router.get("/status", response_model=GameStateResponse)
async def get_server_status():
    active_users = await RedisService.get_active_users_count()
    return GameStateResponse(available_slots=100 - active_users, max_users=100)
