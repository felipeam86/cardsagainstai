import os
import anthropic
from typing import List
from fastapi import HTTPException

class AnthropicService:
    def __init__(self):
        self.client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-haiku-20240307"  # Use the appropriate model version

    async def generate_ai_response(self, black_card: str, white_cards: List[str], ai_personality: str, num_cards: int) -> List[int]:
        prompt = f"""You are playing a game similar to Cards Against Humanity. 
        You have the personality of {ai_personality}.
        The black card is: {black_card}
        Your white cards are:
        {self._format_card_list(white_cards)}
        
        Choose the funniest {num_cards} white card{'s' if num_cards > 1 else ''} to play.
        Only return the number{'s' if num_cards > 1 else ''} of the chosen card{'s' if num_cards > 1 else ''}, separated by commas if more than one.
        For example, if you choose cards 2 and 5, just return: 2,5"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=20,
                messages=[{"role": "user", "content": prompt}]
            )
            chosen_cards = [int(card.strip()) for card in response.content[0].text.strip().split(',')]
            
            # Validate the response
            if len(chosen_cards) != num_cards or any(card < 1 or card > len(white_cards) for card in chosen_cards):
                raise ValueError("Invalid AI response")
            
            return chosen_cards
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating AI response: {str(e)}")

    async def judge_round(self, black_card: str, user_cards: List[str], ai_cards: List[str]) -> tuple[str, str]:
        prompt = f"""You are the judge in a game similar to Cards Against Humanity.
        The black card is: {black_card}
        The human player's white card{'s' if len(user_cards) > 1 else ''}: {' '.join(user_cards)}
        The AI player's white card{'s' if len(ai_cards) > 1 else ''}: {' '.join(ai_cards)}
        
        Determine the winner based on which answer is funnier or more fitting.
        Provide a brief explanation for your decision.
        Return your response in the format: "Winner: [human/ai]\nExplanation: [Your explanation here]" """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.content[0].text.strip().split("\n", 1)
            winner = result[0].split(": ")[1].lower()
            explanation = result[1].split(": ")[1]
            return winner, explanation
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error judging round: {str(e)}")

    def _format_card_list(self, cards: List[str]) -> str:
        return "\n".join(f"{i+1}. {card}" for i, card in enumerate(cards))