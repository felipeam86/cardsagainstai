from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.models import GameSession, User
from ..schemas.history import GameHistoryResponse

router = APIRouter()


@router.get("/history/{user_id}", response_model=list[GameHistoryResponse])
def get_user_game_history(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    games = db.query(GameSession).filter(GameSession.user_id == user_id).all()
    return [
        GameHistoryResponse(
            id=game.id,
            user_id=game.user_id,
            ai_personality_id=game.ai_personality_id,
            start_time=str(game.start_time),
            end_time=str(game.end_time) if game.end_time else None,
        )
        for game in games
    ]
