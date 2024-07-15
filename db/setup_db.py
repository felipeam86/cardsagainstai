from pathlib import Path
import sqlite3

import pandas as pd


# Create a connection to the database
conn_source = sqlite3.connect(Path(__file__).parent / "source.sqlite")
conn_dest = sqlite3.connect(Path(__file__).parent.parent / "cards_against_ai.db")


TABLES_TO_MOVE = {
    "black_cards": ["id", "text", "pick", "watermark"],
    "white_cards": ["id", "text", "watermark"],
}


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

    conn_dest.close()


if __name__ == "__main__":
    setup_db()
