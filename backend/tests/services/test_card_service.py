import pytest
from unittest.mock import Mock
from app.services.card_service import CardService
from app.models.models import BlackCard, WhiteCard, CardSet


@pytest.fixture
def mock_db():
    return Mock()


@pytest.fixture
def card_service(mock_db):
    return CardService(mock_db)


class TestDrawBlackCard:
    def test_draw_black_card_success(self, card_service, mock_db):
        mock_black_card = BlackCard(id=1, text="Test black card", pick=2)
        mock_db.query.return_value.order_by.return_value.first.return_value = (
            mock_black_card
        )

        black_card = card_service.draw_black_card()

        assert isinstance(black_card, BlackCard)
        assert black_card.id == 1
        assert black_card.text == "Test black card"
        assert black_card.pick == 2

    def test_draw_black_card_no_cards(self, card_service, mock_db):
        mock_db.query.return_value.order_by.return_value.first.return_value = None

        with pytest.raises(ValueError, match="No black cards available"):
            card_service.draw_black_card()


class TestDrawWhiteCards:
    def test_draw_white_cards_success(self, card_service, mock_db):
        mock_white_cards = [
            WhiteCard(id=i, text=f"White card {i}") for i in range(1, 6)
        ]
        mock_db.query.return_value.order_by.return_value.limit.return_value.all.return_value = (
            mock_white_cards
        )

        white_cards = card_service.draw_white_cards(5)

        assert len(white_cards) == 5
        assert all(isinstance(card, WhiteCard) for card in white_cards)

    def test_draw_white_cards_not_enough_cards(self, card_service, mock_db):
        mock_white_cards = [
            WhiteCard(id=i, text=f"White card {i}") for i in range(1, 4)
        ]
        mock_db.query.return_value.order_by.return_value.limit.return_value.all.return_value = (
            mock_white_cards
        )

        with pytest.raises(ValueError, match="Not enough white cards available"):
            card_service.draw_white_cards(5)


class TestGetCardSets:
    def test_get_card_sets_success(self, card_service, mock_db):
        mock_card_sets = [CardSet(id=i, name=f"Card Set {i}") for i in range(1, 4)]
        mock_db.query.return_value.all.return_value = mock_card_sets

        card_sets = card_service.get_card_sets()

        assert len(card_sets) == 3
        assert all(isinstance(card_set, CardSet) for card_set in card_sets)

    def test_get_card_sets_empty(self, card_service, mock_db):
        mock_db.query.return_value.all.return_value = []

        card_sets = card_service.get_card_sets()

        assert len(card_sets) == 0
