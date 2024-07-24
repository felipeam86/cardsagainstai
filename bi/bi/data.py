from pathlib import Path
import unicodedata

import pandas as pd

COMMITS_CSV = Path(__file__).parent.parent.parent / "commits.csv"
FIRST_COMMIT_PROMPTS = 10


BRANCHES = {
    "37d4bcc25d2a4887375c56efc20afff68796488a": "frontend-v1",
    "1ff66da0b6be18c460fe5a5d6619f63902445669": "frontend-v1",
    "8570a2fad01d177f9e6117a8e11eb45d2892c2d5": "backend-v1",
    "dea8369ad7ba0dfcc8ffeafec7ced6e4b8273554": "backend-v1",
    "1a5622bcdd0b1513526b7617be1ff10a81cbfae9": "backend-v1",
}


def split_emojis(text):
    # Use a list comprehension to split the text into a list of characters
    return [char for char in text if unicodedata.category(char).startswith("So")]


def read_commits():
    df = (
        pd.read_csv(COMMITS_CSV)
        .assign(
            lines_net=lambda df: df["lines_added"] - df["lines_removed"],
            branch=lambda df: df.commit_hash.map(BRANCHES).fillna("main"),
            is_deadend=lambda df: df["type"].str.contains("☠️"),
            type=lambda df: df["type"].map(split_emojis),
            main_type=lambda df: df["type"].map(lambda t: "🗃" if "🗃" in t else t[0]),
            tools=lambda df: df["tools"].str.split(","),
            prompts=lambda df: df["prompts"].fillna(FIRST_COMMIT_PROMPTS).astype(int),
            corrections=lambda df: df["corrections"].fillna(0).astype(int),
            is_deprecated=lambda df: df.branch.map(
                df.groupby("branch").is_deadend.any()
            ),
        )
        .sort_values("date")
        .reset_index(drop=True)
    )
    return df
