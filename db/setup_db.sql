DROP TABLE IF EXISTS black_cards;
DROP TABLE IF EXISTS white_cards;
DROP TABLE IF EXISTS card_set;
DROP TABLE IF EXISTS card_set_black_card;
DROP TABLE IF EXISTS card_set_white_card;

CREATE TABLE black_cards (
    id INTEGER,
    text VARCHAR,
    pick INTEGER NOT NULL,
    watermark VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE white_cards (
    id INTEGER,
    text VARCHAR,
    watermark VARCHAR,
    PRIMARY KEY (id)
);

-- The game provides different sets or bundles of cards
CREATE TABLE card_set (
    id INTEGER,
    name VARCHAR,
    PRIMARY KEY (id)
);

-- Card set many-to-many relationship to black cards
CREATE TABLE card_set_black_card (
    card_set_id INTEGER NOT NULL,
    black_card_id INTEGER NOT NULL,
    PRIMARY KEY (card_set_id, black_card_id),
    FOREIGN KEY (card_set_id) REFERENCES card_set(id),
    FOREIGN KEY (black_card_id) REFERENCES black_cards(id)
);

-- Card set many-to-many relationship to white cards
CREATE TABLE card_set_white_card (
    card_set_id INTEGER NOT NULL,
    white_card_id INTEGER NOT NULL,
    PRIMARY KEY (card_set_id, white_card_id),
    FOREIGN KEY (card_set_id) REFERENCES card_set(id),
    FOREIGN KEY (white_card_id) REFERENCES white_cards(id)
);
