# tests/services/test_redis_service.py
import pytest
from unittest.mock import AsyncMock
import json
from app.services.redis_service import RedisService


@pytest.fixture
def mock_redis():
    return AsyncMock()


@pytest.fixture
def redis_service(mock_redis):
    return RedisService(mock_redis)


class TestSetGameState:
    @pytest.mark.asyncio
    async def test_set_game_state_success(self, redis_service, mock_redis):
        game_id = "1"
        state = {"status": "in_progress", "current_round": 1}

        await redis_service.set_game_state(game_id, state)

        mock_redis.hmset.assert_called_once_with(
            f"game:{game_id}", {k: json.dumps(v) for k, v in state.items()}
        )


class TestGetGameState:
    @pytest.mark.asyncio
    async def test_get_game_state_success(self, redis_service, mock_redis):
        game_id = "1"
        mock_redis.hgetall.return_value = {
            b"status": b'"in_progress"',
            b"current_round": b"1",
        }

        state = await redis_service.get_game_state(game_id)

        assert state == {"status": "in_progress", "current_round": 1}
        mock_redis.hgetall.assert_called_once_with(f"game:{game_id}")

    @pytest.mark.asyncio
    async def test_get_game_state_not_found(self, redis_service, mock_redis):
        game_id = "1"
        mock_redis.hgetall.return_value = {}

        state = await redis_service.get_game_state(game_id)

        assert state == {}
        mock_redis.hgetall.assert_called_once_with(f"game:{game_id}")


class TestDeleteGameState:
    @pytest.mark.asyncio
    async def test_delete_game_state_success(self, redis_service, mock_redis):
        game_id = "1"

        await redis_service.delete_game_state(game_id)

        mock_redis.delete.assert_called_once_with(f"game:{game_id}")


class TestAddActiveUser:
    @pytest.mark.asyncio
    async def test_add_active_user_success(self, redis_service, mock_redis):
        user_id = "1"

        await redis_service.add_active_user(user_id)

        mock_redis.sadd.assert_called_once_with("active_users", user_id)


class TestRemoveActiveUser:
    @pytest.mark.asyncio
    async def test_remove_active_user_success(self, redis_service, mock_redis):
        user_id = "1"

        await redis_service.remove_active_user(user_id)

        mock_redis.srem.assert_called_once_with("active_users", user_id)


class TestGetActiveUsersCount:
    @pytest.mark.asyncio
    async def test_get_active_users_count_success(self, redis_service, mock_redis):
        mock_redis.scard.return_value = 5

        count = await redis_service.get_active_users_count()

        assert count == 5
        mock_redis.scard.assert_called_once_with("active_users")
