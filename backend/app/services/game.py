from datetime import datetime, timezone
from typing import List, Tuple

from sqlmodel import Session, select
from app.db.models import (
    GameSession,
    GameRound,
    CardPlay,
    BlackCard,
    WhiteCard,
    AIPersonality,
    User,
)
from app.services.anthropic import AnthropicService
from app.services.card_manager import CardManagerService


class GameService:
    def __init__(
        self,
        db: Session,
        anthropic_service: AnthropicService,
        card_manager: CardManagerService,
    ):
        self.db = db
        self.anthropic_service = anthropic_service
        self.card_manager = card_manager

    async def create_game_session(
        self, username: str, ai_personality_id: int
    ) -> GameSession:
        ai_personality = self.db.get(AIPersonality, ai_personality_id)
        user = self._get_or_make_user_id_by_username(username=username)
        if not ai_personality:
            raise ValueError("Invalid AI personality ID")

        game_session = GameSession(user_id=user.id, ai_personality_id=ai_personality_id)
        self.db.add(game_session)
        self.db.commit()
        self.db.refresh(game_session)
        return game_session

    async def create_game_round(
        self, game_session_id: int
    ) -> Tuple[GameRound, BlackCard, List[WhiteCard]]:
        game_session = self.db.get(GameSession, game_session_id)
        if not game_session:
            raise ValueError("Invalid game session ID")

        black_card = self.card_manager.draw_black_card()

        (
            previous_round_number,
            user_score,
            ai_score,
        ) = self.get_latest_game_round_information(game_session_id=game_session_id)
        game_round = GameRound(
            game_session_id=game_session_id,
            round_number=previous_round_number + 1,
            black_card_id=black_card.id,
            user_score=user_score,
            ai_score=ai_score,
            winner=None,
        )
        self.db.add(game_round)
        self.db.commit()
        self.db.refresh(game_round)
        self.db.refresh(black_card)
        white_cards = self.card_manager.draw_white_cards(10)

        return game_round, black_card, white_cards

    async def submit_game_round(
        self,
        round_id: int,
        user_card_ids: List[int],
        white_card_ids: List[int],
    ) -> Tuple[GameRound, List[WhiteCard]]:
        game_round = self._get_round(round_id)
        black_card = self._get_black_card(game_round.black_card_id)
        user_cards = self._get_white_cards_from_ids(user_card_ids)
        white_cards = self._get_white_cards_from_ids(white_card_ids)

        ai_personality = self._get_ai_personality_by_session_id(
            game_round.game_session_id
        )
        ai_chosen_cards = await self.anthropic_service.generate_ai_response(
            black_card=black_card,
            white_cards=white_cards,
            ai_personality=ai_personality,
        )
        tie = all(
            [
                user_card.id == ai_card.id
                for user_card, ai_card in zip(user_cards, ai_chosen_cards)
            ]
        )
        if tie:
            winner = "tie"
            explanation = "The AI and human both played the same cards... so boring"
        else:
            winner, explanation = await self.anthropic_service.judge_round(
                black_card=black_card,
                user_cards=user_cards,
                ai_cards=ai_chosen_cards,
            )

        game_round.winner = winner
        game_round.judge_explanation = explanation
        if winner == "human":
            game_round.user_score += 1
        elif winner == "ai":
            game_round.ai_score += 1

        for i, (user_card, ai_card) in enumerate(zip(user_cards, ai_chosen_cards)):
            card_play = CardPlay(
                round_id=round_id,
                user_card_id=user_card.id,
                ai_card_id=ai_card.id,
                play_order=i,
            )
            self.db.add(card_play)

        self.db.commit()
        self.db.refresh(game_round)
        self.db.refresh(black_card)
        for card in white_cards:
            self.db.refresh(card)
        for card in user_cards:
            self.db.refresh(card)

        return (game_round, ai_chosen_cards)

    def end_game_session(self, game_session_id: int) -> GameSession:
        game_session = self.db.get(GameSession, game_session_id)
        if not game_session:
            raise ValueError("Invalid game session ID")

        game_session.end_time = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(game_session)
        return game_session

    def _get_or_make_user_id_by_username(self, username: str) -> User:
        user = self.db.exec(select(User).where(User.username == username)).first()
        if not user:
            user = User(username=username)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user

    def get_latest_game_round_information(
        self,
        game_session_id: int,
    ) -> Tuple[int, int, int]:
        statement = (
            select(GameRound)
            .where(GameRound.game_session_id == game_session_id)
            .order_by(GameRound.round_number.desc())
            .limit(1)
        )

        game_round = self.db.exec(statement).first()
        if not game_round:
            return 0, 0, 0
        return game_round.round_number, game_round.user_score, game_round.ai_score

    def _get_round(self, round_id: int) -> GameRound:
        game_round = self.db.get(GameRound, round_id)
        if not game_round:
            raise ValueError("Invalid round ID")
        return game_round

    def _get_black_card(self, black_card_id: int) -> BlackCard:
        black_card = self.db.get(BlackCard, black_card_id)
        if not black_card:
            raise ValueError("Invalid black card ID")
        return black_card

    def _get_white_cards_from_ids(self, card_ids: List[int]) -> List[WhiteCard]:

        white_cards = []
        for card_id in card_ids:
            card = self.db.get(WhiteCard, card_id)
            if not card:
                raise ValueError(f"Invalid card ID {card_id}")
            white_cards.append(card)

        return white_cards

    def _get_ai_personality_by_session_id(self, game_session_id: int) -> AIPersonality:
        # Create a select statement that joins the necessary tables
        game_session = self.db.get(GameSession, game_session_id)
        if game_session is None:
            raise ValueError(f"No game session found for ID {game_session_id}")
        ai_personality = self.db.get(AIPersonality, game_session.ai_personality_id)
        if ai_personality is None:
            raise ValueError(
                f"No AI personality found for game session ID {game_session_id}"
            )
        else:
            return ai_personality
