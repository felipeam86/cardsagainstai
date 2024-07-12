from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.models import GameSession, GameRound, CardPlay, User, AIPersonality
from .redis_service import RedisService
from .ai_service import AIService
from .card_service import CardService


class GameService:
    def __init__(
        self,
        db: Session,
        redis: RedisService,
        ai_service: AIService,
        card_service: CardService,
    ):
        self.db = db
        self.redis = redis
        self.ai_service = ai_service
        self.card_service = card_service

    async def create_game(self, user_id: int, ai_personality_id: int) -> GameSession:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        ai_personality = (
            self.db.query(AIPersonality)
            .filter(AIPersonality.id == ai_personality_id)
            .first()
        )
        if not ai_personality:
            raise ValueError(f"AI Personality with id {ai_personality_id} not found")

        game_session = GameSession(user_id=user_id, ai_personality_id=ai_personality_id)
        self.db.add(game_session)
        self.db.commit()
        self.db.refresh(game_session)

        await self.redis.set_game_state(
            str(game_session.id),
            {"status": "created", "current_round": 0, "user_score": 0, "ai_score": 0},
        )

        return game_session

    async def start_game(self, game_id: int) -> GameSession:
        game_session = (
            self.db.query(GameSession).filter(GameSession.id == game_id).first()
        )
        if not game_session:
            raise ValueError("Game session not found")

        # Initialize game state, draw initial cards, etc.
        await self.redis.set_game_state(
            str(game_id),
            {
                "status": "in_progress",
                "current_round": 1,
                "user_score": 0,
                "ai_score": 0,
            },
        )

        # Create first round
        black_card = self.card_service.draw_black_card()
        new_round = GameRound(
            game_session_id=game_id,
            round_number=1,
            black_card_id=black_card.id,
            user_score=0,
            ai_score=0,
        )
        self.db.add(new_round)
        self.db.commit()

        return game_session

    async def submit_cards(
        self, round_id: int, user_card_ids: list[int], ai_card_ids: list[int]
    ) -> GameRound:
        game_round = self.db.query(GameRound).filter(GameRound.id == round_id).first()
        if not game_round:
            raise ValueError("Game round not found")

        for i, (user_card_id, ai_card_id) in enumerate(zip(user_card_ids, ai_card_ids)):
            card_play = CardPlay(
                round_id=round_id,
                user_card_id=user_card_id,
                ai_card_id=ai_card_id,
                play_order=i + 1,
            )
            self.db.add(card_play)

        self.db.commit()

        winner, explanation = await self.ai_service.judge_round(
            game_round, user_card_ids, ai_card_ids
        )

        game_round.winner = winner
        game_round.judge_explanation = explanation
        if winner == "user":
            game_round.user_score = game_round.user_score + 1
        else:
            game_round.ai_score = game_round.ai_score + 1

        self.db.commit()

        return game_round

    async def get_round_result(self, round_id: int) -> GameRound:
        game_round = self.db.query(GameRound).filter(GameRound.id == round_id).first()
        if not game_round:
            raise ValueError("Game round not found")
        return game_round

    async def next_round(self, game_id: int) -> GameRound:
        game_session = (
            self.db.query(GameSession).filter(GameSession.id == game_id).first()
        )
        if not game_session:
            raise ValueError("Game session not found")

        current_round = (
            self.db.query(GameRound)
            .filter(GameRound.game_session_id == game_id)
            .order_by(GameRound.round_number.desc())
            .first()
        )

        if current_round.round_number >= 10:
            # End the game
            game_session.end_time = func.now()
            await self.redis.set_game_state(str(game_id), {"status": "completed"})
            self.db.commit()
            return None

        # Create new round
        new_round_number = current_round.round_number + 1
        black_card = self.card_service.draw_black_card()
        new_round = GameRound(
            game_session_id=game_id,
            round_number=new_round_number,
            black_card_id=black_card.id,
            user_score=current_round.user_score,
            ai_score=current_round.ai_score,
        )
        self.db.add(new_round)
        self.db.commit()

        await self.redis.set_game_state(
            str(game_id),
            {
                "status": "in_progress",
                "current_round": new_round_number,
                "user_score": current_round.user_score,
                "ai_score": current_round.ai_score,
            },
        )

        return new_round
