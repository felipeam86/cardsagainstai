from fastapi import Depends
from sqlalchemy.orm import Session
from redis import Redis
from ..db.session import get_db
from ..core.config import settings
from ..services.game_service import GameService
from ..services.ai_service import AIService
from ..services.card_service import CardService
from ..services.redis_service import RedisService

redis_client = Redis.from_url(settings.REDIS_URL)


def get_redis_service():
    return RedisService(redis_client)


def get_card_service(db: Session = Depends(get_db)):
    return CardService(db)


def get_ai_service(db: Session = Depends(get_db)):
    return AIService(db, settings.ANTHROPIC_API_KEY)


def get_game_service(
    db: Session = Depends(get_db),
    redis_service: RedisService = Depends(get_redis_service),
    ai_service: AIService = Depends(get_ai_service),
    card_service: CardService = Depends(get_card_service),
):
    return GameService(db, redis_service, ai_service, card_service)
