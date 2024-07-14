from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.models import AIPersonality, User
from ..schemas.ai_personalities import AIPersonalityInput, AIPersonalityResponse

router = APIRouter()


@router.get("/ai-personalities", response_model=list[AIPersonalityResponse])
def get_ai_personalities(db: Session = Depends(get_db)):
    return db.query(AIPersonality).all()


@router.post("/ai-personalities", response_model=AIPersonalityResponse)
def create_ai_personality(
    personality: AIPersonalityInput, user_id: int, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_personality = AIPersonality(**personality.model_dump(), created_by_id=user_id)
    db.add(new_personality)
    db.commit()
    db.refresh(new_personality)
    return new_personality
