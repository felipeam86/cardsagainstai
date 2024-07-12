from anthropic import Anthropic
from ..models.models import GameRound, BlackCard, WhiteCard
from sqlalchemy.orm import Session


class AIService:
    def __init__(self, db: Session, anthropic_api_key: str):
        self.db = db
        self.client = Anthropic(api_key=anthropic_api_key)

    async def generate_ai_play(
        self, black_card: BlackCard, white_cards: list[WhiteCard], num_cards: int
    ) -> list[int]:
        if len(white_cards) < num_cards:
            raise ValueError("Not enough white cards available")

        prompt = f"Given the black card: '{black_card.text}', choose {num_cards} white card(s) that would be the funniest combination. Here are the available white cards:\n"
        for i, card in enumerate(white_cards):
            prompt += f"{i+1}. {card.text}\n"
        prompt += f"\nRespond with only the numbers of the {num_cards} chosen card(s), separated by commas."

        response = self.client.completions.create(
            model="claude-2", prompt=prompt, max_tokens_to_sample=20
        )

        try:
            chosen_indices = [int(i.strip()) for i in response.completion.split(",")]
            if len(chosen_indices) != num_cards:
                raise ValueError("Invalid number of cards selected")
            return [white_cards[i - 1].id for i in chosen_indices]
        except ValueError:
            raise ValueError("Invalid response from AI")

    async def judge_round(
        self, game_round: GameRound, user_card_ids: list[int], ai_card_ids: list[int]
    ) -> tuple[str, str]:
        black_card = (
            self.db.query(BlackCard)
            .filter(BlackCard.id == game_round.black_card_id)
            .first()
        )
        user_cards = (
            self.db.query(WhiteCard).filter(WhiteCard.id.in_(user_card_ids)).all()
        )
        ai_cards = self.db.query(WhiteCard).filter(WhiteCard.id.in_(ai_card_ids)).all()

        prompt = f"Judge this Cards Against Humanity round:\n\nBlack Card: {black_card.text}\n\n"
        prompt += f"Player's Cards: {', '.join([card.text for card in user_cards])}\n"
        prompt += f"AI's Cards: {', '.join([card.text for card in ai_cards])}\n\n"
        prompt += "Which combination is funnier? Respond with either 'user' or 'ai', followed by a brief explanation."

        response = self.client.completions.create(
            model="claude-2", prompt=prompt, max_tokens_to_sample=100
        )

        winner, explanation = response.completion.split("\n", 1)
        winner = winner.strip().lower()
        if winner not in ["user", "ai"]:
            raise ValueError("Invalid winner")
        explanation = explanation.strip()

        return winner, explanation
