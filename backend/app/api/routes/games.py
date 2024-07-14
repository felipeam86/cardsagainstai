from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.models import GameSession, User, AIPersonality
from ...services.game_service import GameService
from ...services.redis_service import RedisService
from ..schemas.games import (
    GameSessionCreate,
    GameSessionResponse,
    GameStateResponse,
    CardSubmission,
    GameRound,
)

router = APIRouter()


def get_game_service(db: Session = Depends(get_db)):
    redis_service = RedisService(
        db.connection().engine.redis_connection
    )  # Assuming Redis connection is available through the database engine
    return GameService(db, redis_service)


@router.post("/game-sessions", response_model=GameSessionResponse)
async def create_game_session(
    game: GameSessionCreate, game_service: GameService = Depends(get_game_service)
):
    return await game_service.create_game(game.user_id, game.ai_personality_id)


@router.get("/game-sessions/{session_id}", response_model=GameSessionResponse)
async def get_game_session(
    session_id: int, game_service: GameService = Depends(get_game_service)
):
    return await game_service.get_game_session(session_id)


@router.post("/game-sessions/{session_id}/start")
async def start_game_session(
    session_id: int, game_service: GameService = Depends(get_game_service)
):
    return await game_service.start_game(session_id)


@router.post("/game-rounds/{round_id}/submit")
async def submit_card_plays(
    round_id: int,
    submission: CardSubmission,
    game_service: GameService = Depends(get_game_service),
):
    return await game_service.submit_cards(
        round_id, submission.user_card_ids, submission.ai_card_ids
    )


@router.get("/game-rounds/{round_id}/result", response_model=GameRound)
async def get_round_result(
    round_id: int, game_service: GameService = Depends(get_game_service)
):
    return await game_service.get_round_result(round_id)


@router.get("/status", response_model=GameStateResponse)
async def get_server_status(game_service: GameService = Depends(get_game_service)):
    redis_service = game_service.redis
    active_users = await redis_service.get_active_users_count()
    return GameStateResponse(available_slots=100 - active_users, max_users=100)
