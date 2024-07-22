from pathlib import Path
import sqlite3

import pandas as pd


# Create a connection to the database
conn_source = sqlite3.connect(Path(__file__).parent / "source.sqlite")
conn_dest = sqlite3.connect(Path(__file__).parent.parent / "cards_against_ai.db")


TABLES_TO_MOVE = {
    "black_cards": ["id", "text", "pick", "watermark", "category"],
    "white_cards": ["id", "text", "watermark", "category"],
}

EXTRA_WHITE_CARDS = list(
    (Path(__file__).parent / "colombian_cards").glob("tarjetas-blancas*.csv")
)
EXTRA_BLACK_CARDS = list(
    (Path(__file__).parent / "colombian_cards").glob("tarjetas-negras*.csv")
)


def setup_db():

    # Create the tables
    cur = conn_dest.cursor()
    setup_script = (Path(__file__).parent / "setup_db.sql").read_text()
    cur.executescript(setup_script)
    conn_dest.commit()

    # Move the data
    for table, columns in TABLES_TO_MOVE.items():
        columns_str = ", ".join(columns)
        df_source = pd.read_sql(f"SELECT {columns_str} FROM {table}", conn_source)
        df_source.to_sql(table, conn_dest, index=False, if_exists="append")


def insert_extra_cards():
    df_black = pd.concat(
        [
            pd.read_csv(csv_file).assign(
                watermark=csv_file.name.split(".")[0].split("-")[-1].upper(),
                category="SAFE",
                language="ES",
            )
            for csv_file in EXTRA_BLACK_CARDS
        ]
    )

    df_white = pd.concat(
        [
            pd.read_csv(csv_file).assign(
                watermark=csv_file.name.split(".")[0].split("-")[-1].upper(),
                category="SAFE",
                language="ES",
            )
            for csv_file in EXTRA_WHITE_CARDS
        ]
    )
    df_black.to_sql("black_cards", con=conn_dest, index=False, if_exists="append")
    df_white.to_sql("white_cards", con=conn_dest, index=False, if_exists="append")


if __name__ == "__main__":
    setup_db()
    insert_extra_cards()
    conn_dest.close()
