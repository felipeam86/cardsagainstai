import sqlite3

from dotenv import load_dotenv
from openai import OpenAI
from tqdm.auto import tqdm

# Load environment variables
load_dotenv()


# Connect to the SQLite database
conn = sqlite3.connect("source.sqlite")
cursor = conn.cursor()


PROMPT = """
You are tasked with evaluating a given text to determine if it is Not Safe For Work (NSFW) or offensive.
NSFW content typically includes explicit sexual references, graphic violence, or other material unsuitable for a professional or public setting.
Offensive content may include hate speech, extreme political views, discriminatory language, or other text that could be considered highly inappropriate or hurtful.

Here is the text to evaluate:

<text_to_evaluate>
{text}
</text_to_evaluate>

Carefully read and analyze the text above. Consider the following aspects:
1. Presence of explicit sexual content
2. Graphic depictions of violence
3. Use of profanity or vulgar language
4. Hate speech or discriminatory language
5. Extreme political views
6. Other potentially offensive or inappropriate content

After your analysis, provide only your final judgment following format:
NSFW: if the text is Not Safe For Work
OFFENSIVE: if the text is offensive but not necessarily NSFW
SAFE: if the text is neither NSFW nor offensive

If the text is both NSFW and offensive, use the [NSFW] judgment.

Begin your evaluation now.
"""


client = OpenAI()


def check_content(text):
    """
    Check if the text is offensive or inappropriate using OpenAI's API.
    """
    prompt = PROMPT.format(text=text)

    nsfw = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return nsfw.choices[0].message.content


def get_cards(table_name):
    cursor.execute(f"SELECT id, text FROM {table_name}")
    return cursor.fetchall()


def process_cards(table_name):
    """
    Process cards from the given table, check content, and update the category.
    """
    cards = get_cards(table_name)

    for card_id, card_text in tqdm(cards):
        category = check_content(card_text)
        cursor.execute(
            f"UPDATE {table_name} SET category = ? WHERE id = ?", (category, card_id)
        )
        conn.commit()
        print(f"Processed {table_name} card {card_id}: {category}")


if __name__ == "__main__":
    # Process black cards
    process_cards("black_cards")

    # Process white cards
    process_cards("white_cards")

    # Close the database connection
    conn.close()

    print("All cards have been processed and categorized.")
