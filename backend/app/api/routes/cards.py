from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models.models import BlackCard, WhiteCard
from ..schemas.cards import BlackCard, WhiteCard


from random import choice

router = APIRouter()


@router.get("/cards/black", response_model=BlackCard)
def get_black_card(db: Session = Depends(get_db)):
    black_cards = db.query(BlackCard).all()
    if not black_cards:
        raise HTTPException(status_code=404, detail="No black cards available")
    card = choice(black_cards)
    return CardResponse(
        id=card.id, text=card.text, pick=card.pick, watermark=card.watermark
    )


@router.get("/cards/white", response_model=list[WhiteCard])
def get_white_cards(db: Session = Depends(get_db)):
    white_cards = db.query(WhiteCard).all()
    if len(white_cards) < 10:
        raise HTTPException(status_code=404, detail="Not enough white cards available")
    selected_cards = [choice(white_cards) for _ in range(10)]
    return [
        CardResponse(id=card.id, text=card.text, watermark=card.watermark)
        for card in selected_cards
    ]
