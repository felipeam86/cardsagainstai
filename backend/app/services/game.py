from sqlmodel import Session, select
from app.db.models import GameSession, GameRound, CardPlay, BlackCard, WhiteCard, AIPersonality
from app.services.anthropic import AnthropicService
from app.services.card_manager import CardManagerService
from typing import List, Tuple

class GameService:
    def __init__(self, db: Session, anthropic_service: AnthropicService, card_manager: CardManagerService):
        self.db = db
        self.anthropic_service = anthropic_service
        self.card_manager = card_manager

    async def create_game_session(self, user_id: int, ai_personality_id: int) -> GameSession:
        ai_personality = self.db.exec(select(AIPersonality).where(AIPersonality.id == ai_personality_id)).first()
        if not ai_personality:
            raise ValueError("Invalid AI personality ID")

        game_session = GameSession(user_id=user_id, ai_personality_id=ai_personality_id)
        self.db.add(game_session)
        self.db.commit()
        self.db.refresh(game_session)
        return game_session

    async def start_round(self, game_session_id: int) -> Tuple[GameRound, BlackCard, List[WhiteCard]]:
        game_session = self.db.get(GameSession, game_session_id)
        if not game_session:
            raise ValueError("Invalid game session ID")

        black_card = self.card_manager.draw_black_card()
        user_white_cards = self.card_manager.draw_white_cards(10 - len(self.get_user_hand(game_session_id)))

        round_number = len(game_session.game_rounds) + 1
        game_round = GameRound(
            game_session_id=game_session_id,
            round_number=round_number,
            black_card_id=black_card.id,
            user_score=0,
            ai_score=0,
            winner=""
        )
        self.db.add(game_round)
        self.db.commit()
        self.db.refresh(game_round)

        return game_round, black_card, user_white_cards

    async def play_round(self, round_id: int, user_card_ids: List[int]) -> Tuple[str, List[str], List[str], str]:
        game_round = self.db.get(GameRound, round_id)
        if not game_round:
            raise ValueError("Invalid round ID")

        black_card = game_round.black_card
        user_cards = [self.db.get(WhiteCard, card_id) for card_id in user_card_ids]
        ai_cards = self.card_manager.draw_white_cards(10)  # Draw 10 cards for AI to choose from

        ai_personality = game_round.game_session.ai_personality
        ai_card_indices = await self.anthropic_service.generate_ai_response(
            black_card.text,
            [card.text for card in ai_cards],
            ai_personality.name,
            black_card.pick
        )

        ai_chosen_cards = [ai_cards[i-1] for i in ai_card_indices]

        winner, explanation = await self.anthropic_service.judge_round(
            black_card.text,
            [card.text for card in user_cards],
            [card.text for card in ai_chosen_cards]
        )

        game_round.winner = winner
        game_round.judge_explanation = explanation
        if winner == "user":
            game_round.user_score = 1
        else:
            game_round.ai_score = 1

        for i, (user_card, ai_card) in enumerate(zip(user_cards, ai_chosen_cards)):
            card_play = CardPlay(
                round_id=round_id,
                user_card_id=user_card.id,
                ai_card_id=ai_card.id,
                play_order=i
            )
            self.db.add(card_play)

        self.db.commit()
        self.db.refresh(game_round)

        return black_card.text, [card.text for card in user_cards], [card.text for card in ai_chosen_cards], explanation


    def get_user_hand(self, game_session_id: int) -> List[WhiteCard]:
        game_session = self.db.get(GameSession, game_session_id)
        if not game_session:
            raise ValueError("Invalid game session ID")

        played_card_ids = self.db.exec(
            select(CardPlay.user_card_id)
            .join(GameRound, CardPlay.round_id == GameRound.id)
            .where(GameRound.game_session_id == game_session_id)
        ).all()

        return self.db.exec(
            select(WhiteCard)
            .where(WhiteCard.id.not_in(played_card_ids))
            .limit(10)
        ).all()

    def end_game(self, game_session_id: int) -> GameSession:
        game_session = self.db.get(GameSession, game_session_id)
        if not game_session:
            raise ValueError("Invalid game session ID")

        game_session.end_time = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(game_session)
        return game_session