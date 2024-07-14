from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...services.card_service import CardService
from ..schemas.cards import BlackCard, WhiteCard

router = APIRouter()


def get_card_service(db: Session = Depends(get_db)):
    return CardService(db)


@router.get("/cards/black", response_model=BlackCard)
def get_black_card(card_service: CardService = Depends(get_card_service)):
    return card_service.draw_black_card()


@router.get("/cards/white", response_model=list[WhiteCard])
def get_white_cards(card_service: CardService = Depends(get_card_service)):
    return card_service.draw_white_cards(10)  # Draw 10 cards as per game rules
