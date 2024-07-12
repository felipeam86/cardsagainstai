import json
from redis import Redis


class RedisService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def set_game_state(self, game_id: str, state: dict):
        await self.redis.hmset(
            f"game:{game_id}", {k: json.dumps(v) for k, v in state.items()}
        )

    async def get_game_state(self, game_id: str) -> dict:
        state = await self.redis.hgetall(f"game:{game_id}")
        return {k.decode(): json.loads(v.decode()) for k, v in state.items()}

    async def delete_game_state(self, game_id: str):
        await self.redis.delete(f"game:{game_id}")

    async def add_active_user(self, user_id: str):
        await self.redis.sadd("active_users", user_id)

    async def remove_active_user(self, user_id: str):
        await self.redis.srem("active_users", user_id)

    async def get_active_users_count(self) -> int:
        return await self.redis.scard("active_users")
