import pytest
from unittest.mock import Mock, patch
from app.services.ai_service import AIService
from app.models.models import GameRound, BlackCard, WhiteCard


@pytest.fixture
def mock_db():
    return Mock()


@pytest.fixture
def mock_anthropic():
    with patch("app.services.ai_service.Anthropic") as mock:
        yield mock


@pytest.fixture
def ai_service(mock_db, mock_anthropic):
    service = AIService(mock_db, "mock_api_key")
    service.client = mock_anthropic.return_value
    return service


class TestGenerateAIPlay:
    @pytest.mark.asyncio
    async def test_generate_ai_play_success(self, ai_service):
        black_card = BlackCard(id=1, text="Test black card", pick=2)
        white_cards = [WhiteCard(id=i, text=f"White card {i}") for i in range(1, 6)]

        ai_service.client.completions.create.return_value.completion = "1, 3"
        result = await ai_service.generate_ai_play(black_card, white_cards, 2)

        assert result == [1, 3]
        assert len(result) == black_card.pick

    @pytest.mark.asyncio
    async def test_generate_ai_play_invalid_response(self, ai_service):
        black_card = BlackCard(id=1, text="Test black card", pick=2)
        white_cards = [WhiteCard(id=i, text=f"White card {i}") for i in range(1, 6)]

        ai_service.client.completions.create.return_value.completion = (
            "invalid response"
        )
        with pytest.raises(ValueError, match="Invalid response from AI"):
            await ai_service.generate_ai_play(black_card, white_cards, 2)

    @pytest.mark.asyncio
    async def test_generate_ai_play_not_enough_cards(self, ai_service):
        black_card = BlackCard(id=1, text="Test black card", pick=3)
        white_cards = [WhiteCard(id=i, text=f"White card {i}") for i in range(1, 3)]

        with pytest.raises(ValueError, match="Not enough white cards available"):
            await ai_service.generate_ai_play(black_card, white_cards, 3)


class TestJudgeRound:
    @pytest.mark.asyncio
    async def test_judge_round_user_wins(self, ai_service, mock_db):
        game_round = GameRound(id=1, black_card_id=1)
        user_card_ids = [1, 2]
        ai_card_ids = [3, 4]

        mock_db.query.return_value.filter.return_value.first.return_value = BlackCard(
            id=1, text="Test black card"
        )
        mock_db.query.return_value.filter.return_value.all.side_effect = [
            [WhiteCard(id=1, text="User card 1"), WhiteCard(id=2, text="User card 2")],
            [WhiteCard(id=3, text="AI card 1"), WhiteCard(id=4, text="AI card 2")],
        ]

        ai_service.client.completions.create.return_value.completion = (
            "user\nBecause it's funnier"
        )
        winner, explanation = await ai_service.judge_round(
            game_round, user_card_ids, ai_card_ids
        )

        assert winner == "user"
        assert explanation == "Because it's funnier"

    @pytest.mark.asyncio
    async def test_judge_round_ai_wins(self, ai_service, mock_db):
        game_round = GameRound(id=1, black_card_id=1)
        user_card_ids = [1, 2]
        ai_card_ids = [3, 4]

        mock_db.query.return_value.filter.return_value.first.return_value = BlackCard(
            id=1, text="Test black card"
        )
        mock_db.query.return_value.filter.return_value.all.side_effect = [
            [WhiteCard(id=1, text="User card 1"), WhiteCard(id=2, text="User card 2")],
            [WhiteCard(id=3, text="AI card 1"), WhiteCard(id=4, text="AI card 2")],
        ]

        ai_service.client.completions.create.return_value.completion = (
            "ai\nAI's combination is more clever"
        )
        winner, explanation = await ai_service.judge_round(
            game_round, user_card_ids, ai_card_ids
        )

        assert winner == "ai"
        assert explanation == "AI's combination is more clever"

    @pytest.mark.asyncio
    async def test_judge_round_invalid_response(self, ai_service, mock_db):
        game_round = GameRound(id=1, black_card_id=1)
        user_card_ids = [1, 2]
        ai_card_ids = [3, 4]

        mock_db.query.return_value.filter.return_value.first.return_value = BlackCard(
            id=1, text="Test black card"
        )
        mock_db.query.return_value.filter.return_value.all.side_effect = [
            [WhiteCard(id=1, text="User card 1"), WhiteCard(id=2, text="User card 2")],
            [WhiteCard(id=3, text="AI card 1"), WhiteCard(id=4, text="AI card 2")],
        ]

        ai_service.client.completions.create.return_value.completion = (
            "invalid\nInvalid response"
        )
        with pytest.raises(ValueError, match="Invalid winner"):
            await ai_service.judge_round(game_round, user_card_ids, ai_card_ids)
