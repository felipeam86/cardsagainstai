from sqlmodel import Session, select
from app.db.models import BlackCard, WhiteCard
from typing import List
import random


class CardManagerService:
    def __init__(self, db: Session):
        self.db = db

    def draw_black_card(self) -> BlackCard:
        black_cards = self.db.exec(select(BlackCard)).all()
        return random.choice(black_cards)

    def draw_white_cards(self, count: int) -> List[WhiteCard]:
        white_cards = self.db.exec(
            select(WhiteCard).where(WhiteCard.watermark == "US")
        ).all()
        return random.sample(white_cards, count)
