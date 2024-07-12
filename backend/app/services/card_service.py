from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from ..models.models import BlackCard, WhiteCard, CardSet


class CardService:
    def __init__(self, db: Session):
        self.db = db

    def draw_black_card(self) -> BlackCard:
        card = self.db.query(BlackCard).order_by(func.random()).first()
        if not card:
            raise ValueError("No black cards available")
        return card

    def draw_white_cards(self, count: int) -> list[WhiteCard]:
        cards = self.db.query(WhiteCard).order_by(func.random()).limit(count).all()
        if len(cards) < count:
            raise ValueError("Not enough white cards available")
        return cards

    def get_card_sets(self):
        return self.db.query(CardSet).all()
