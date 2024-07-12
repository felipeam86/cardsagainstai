# tests/services/test_game_service.py
import pytest
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.orm import Session
from app.services.game_service import GameService
from app.models.models import (
    GameSession,
    GameRound,
    CardPlay,
    User,
    AIPersonality,
    BlackCard,
    WhiteCard,
)
from app.services.redis_service import RedisService
from app.services.ai_service import AIService
from app.services.card_service import CardService


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def mock_redis_service():
    return AsyncMock(spec=RedisService)


@pytest.fixture
def mock_ai_service():
    return AsyncMock(spec=AIService)


@pytest.fixture
def mock_card_service():
    return Mock(spec=CardService)


@pytest.fixture
def game_service(mock_db, mock_redis_service, mock_ai_service, mock_card_service):
    return GameService(mock_db, mock_redis_service, mock_ai_service, mock_card_service)


class TestCreateGame:
    @pytest.mark.asyncio
    async def test_create_game_success(self, game_service, mock_db, mock_redis_service):
        user_id, ai_personality_id = 1, 1
        mock_user = Mock(spec=User, id=user_id)
        mock_ai_personality = Mock(spec=AIPersonality, id=ai_personality_id)
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_user,
            mock_ai_personality,
        ]

        game_session = await game_service.create_game(user_id, ai_personality_id)

        assert isinstance(game_session, GameSession)
        assert game_session.user_id == user_id
        assert game_session.ai_personality_id == ai_personality_id
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        mock_redis_service.set_game_state.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_game_user_not_found(self, game_service, mock_db):
        user_id, ai_personality_id = 1, 1
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError, match=f"User with id {user_id} not found"):
            await game_service.create_game(user_id, ai_personality_id)

    @pytest.mark.asyncio
    async def test_create_game_ai_personality_not_found(self, game_service, mock_db):
        user_id, ai_personality_id = 1, 1
        mock_user = Mock(spec=User, id=user_id)
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_user,
            None,
        ]

        with pytest.raises(
            ValueError, match=f"AI Personality with id {ai_personality_id} not found"
        ):
            await game_service.create_game(user_id, ai_personality_id)


class TestStartGame:
    @pytest.mark.asyncio
    async def test_start_game_success(
        self, game_service, mock_db, mock_redis_service, mock_card_service
    ):
        game_id = 1
        mock_game_session = Mock(spec=GameSession, id=game_id)
        mock_db.query.return_value.filter.return_value.first.return_value = (
            mock_game_session
        )
        mock_card_service.draw_black_card.return_value = Mock(spec=BlackCard, id=1)

        result = await game_service.start_game(game_id)

        assert result == mock_game_session
        mock_redis_service.set_game_state.assert_called_once()
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_game_not_found(self, game_service, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(ValueError, match="Game session not found"):
            await game_service.start_game(1)


class TestSubmitCards:
    @pytest.mark.asyncio
    async def test_submit_cards_success(self, game_service, mock_db, mock_ai_service):
        round_id, user_card_ids, ai_card_ids = 1, [1, 2], [3, 4]
        mock_game_round = Mock(spec=GameRound)
        mock_game_round.id = round_id
        mock_game_round.user_score = 0
        mock_game_round.ai_score = 0

        mock_db.query.return_value.filter.return_value.first.return_value = (
            mock_game_round
        )
        mock_ai_service.judge_round.return_value = ("user", "User wins")

        result = await game_service.submit_cards(round_id, user_card_ids, ai_card_ids)

        assert result == mock_game_round
        assert mock_db.add.call_count == len(user_card_ids)
        mock_db.commit.assert_called()
        mock_ai_service.judge_round.assert_called_once_with(
            mock_game_round, user_card_ids, ai_card_ids
        )
        assert result.winner == "user"
        assert result.judge_explanation == "User wins"
        assert result.user_score == 1
        assert result.ai_score == 0

    @pytest.mark.asyncio
    async def test_submit_cards_round_not_found(self, game_service, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(ValueError, match="Game round not found"):
            await game_service.submit_cards(1, [1], [2])


class TestGetRoundResult:
    @pytest.mark.asyncio
    async def test_get_round_result_success(self, game_service, mock_db):
        round_id = 1
        mock_game_round = Mock(spec=GameRound, id=round_id)
        mock_db.query.return_value.filter.return_value.first.return_value = (
            mock_game_round
        )

        result = await game_service.get_round_result(round_id)

        assert result == mock_game_round

    @pytest.mark.asyncio
    async def test_get_round_result_not_found(self, game_service, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(ValueError, match="Game round not found"):
            await game_service.get_round_result(1)


class TestNextRound:
    @pytest.mark.asyncio
    async def test_next_round_success(
        self, game_service, mock_db, mock_redis_service, mock_card_service
    ):
        game_id = 1
        mock_game_session = Mock(spec=GameSession, id=game_id)
        mock_current_round = Mock(
            spec=GameRound, round_number=5, user_score=2, ai_score=3
        )
        mock_db.query.return_value.filter.return_value.first.return_value = (
            mock_game_session
        )
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = (
            mock_current_round
        )
        mock_card_service.draw_black_card.return_value = Mock(spec=BlackCard, id=1)

        result = await game_service.next_round(game_id)

        assert isinstance(result, GameRound)
        assert result.round_number == 6
        assert result.user_score == 2
        assert result.ai_score == 3
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_redis_service.set_game_state.assert_called_once()

    @pytest.mark.asyncio
    async def test_next_round_game_end(self, game_service, mock_db, mock_redis_service):
        game_id = 1
        mock_game_session = Mock(spec=GameSession, id=game_id)
        mock_current_round = Mock(
            spec=GameRound, round_number=10, user_score=5, ai_score=5
        )
        mock_db.query.return_value.filter.return_value.first.return_value = (
            mock_game_session
        )
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = (
            mock_current_round
        )

        result = await game_service.next_round(game_id)

        assert result is None
        assert mock_game_session.end_time is not None
        mock_redis_service.set_game_state.assert_called_once_with(
            str(game_id), {"status": "completed"}
        )

    @pytest.mark.asyncio
    async def test_next_round_game_not_found(self, game_service, mock_db):
        mock_db.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(ValueError, match="Game session not found"):
            await game_service.next_round(1)
