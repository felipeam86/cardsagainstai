import anthropic
from typing import List
from fastapi import HTTPException
from app.core.config import get_settings
from app.db.models import WhiteCard, BlackCard, AIPersonality

settings = get_settings()


class AnthropicService:
    def __init__(self):
        self.client = anthropic.Client(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20240620"  # Use the appropriate model version

    async def generate_ai_response(
        self,
        black_card: BlackCard,
        white_cards: List[WhiteCard],
        ai_personality: AIPersonality,
    ) -> List[WhiteCard]:
        prompt = f"""
        You are playing Cards Against Humanity. 
        You have the personality of {ai_personality.description}.
        The black card is: {black_card.text}
        Your white cards are:
        {self._format_white_card(white_cards)}

        Choose the funniest {black_card.pick} white card{'s' if black_card.pick > 1 else ''} to play. Avoid inappropriate content.
        Only return the number{'s' if black_card.pick > 1 else ''} of the chosen card{'s' if black_card.pick > 1 else ''}, separated by commas if more than one.
        For example, if you choose cards 2 and 5, just return: 2,5
        Go stragight to the point. Do not include any other information or explanation. Just the ids of the chosen cards."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=20,
            messages=[{"role": "user", "content": prompt}],
        )
        chosen_cards = [
            int(card.strip()) for card in response.content[0].text.strip().split(",")
        ]
        chosen_cards = list(filter(lambda c: c.id in chosen_cards, white_cards))

        # Validate the response
        if len(chosen_cards) != black_card.pick:
            raise ValueError("Invalid AI response")

        return chosen_cards

    async def judge_round(
        self,
        black_card: BlackCard,
        user_cards: List[WhiteCard],
        ai_cards: List[WhiteCard],
    ) -> tuple[str, str]:
        prompt = f"""You are the judge in a game similar to Cards Against Humanity.
        The black card is: {black_card.text}
        The human player's white card{'s' if len(user_cards) > 1 else ''}: {', '.join([c.text for c in user_cards])}
        The AI player's white card{'s' if len(ai_cards) > 1 else ''}: {', '.join([c.text for c in ai_cards])}
        
        Determine the winner based on which answer is funnier or more fitting.
        Provide a very brief explanation for your decision and be cocky.
        Return your response in the format: "Winner: [human/ai]\nExplanation: [Your explanation here]" """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}],
            )
            result = response.content[0].text.strip().split("\n", 1)
            winner = result[0].split(": ")[1].lower()
            explanation = result[1].split(": ")[1]
            return winner, explanation
        except Exception as e:
            return (
                "human",
                "I am a lousy LLM that cannot judge a simple card game. The AI wins because I am a failure.",
            )

    def _format_white_card(self, cards: List[WhiteCard]) -> str:
        import json

        text = json.dumps(
            [{"id": card.id, "text": card.text} for card in cards], indent=2
        )
        return text
