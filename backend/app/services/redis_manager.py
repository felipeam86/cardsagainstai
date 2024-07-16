import redis
from app.core.config import get_settings

settings = get_settings()

class RedisManager:
    def __init__(self):
        self.redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

    def get_active_users_count(self) -> int:
        return self.redis.scard("active_users")

    def add_active_user(self, user_id: int):
        self.redis.sadd("active_users", user_id)

    def remove_active_user(self, user_id: int):
        self.redis.srem("active_users", user_id)

    def is_user_active(self, user_id: int) -> bool:
        return self.redis.sismember("active_users", user_id)

    def set_game_state(self, game_id: int, state: dict):
        self.redis.hmset(f"game:{game_id}", state)

    def get_game_state(self, game_id: int) -> dict:
        return self.redis.hgetall(f"game:{game_id}")

    def delete_game_state(self, game_id: int):
        self.redis.delete(f"game:{game_id}")

    def set_user_hand(self, user_id: int, card_ids: List[int]):
        self.redis.delete(f"user_hand:{user_id}")
        self.redis.rpush(f"user_hand:{user_id}", *card_ids)

    def get_user_hand(self, user_id: int) -> List[int]:
        return [int(card_id) for card_id in self.redis.lrange(f"user_hand:{user_id}", 0, -1)]

    def remove_cards_from_user_hand(self, user_id: int, card_ids: List[int]):
        for card_id in card_ids:
            self.redis.lrem(f"user_hand:{user_id}", 0, card_id)