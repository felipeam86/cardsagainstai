-- Drop game-specific tables
DROP TABLE IF EXISTS black_cards;
DROP TABLE IF EXISTS white_cards;
DROP TABLE IF EXISTS card_set;
DROP TABLE IF EXISTS card_set_black_card;
DROP TABLE IF EXISTS card_set_white_card;

-- Create or update game-specific tables
CREATE TABLE IF NOT EXISTS black_cards (
    id INTEGER PRIMARY KEY,
    text VARCHAR NOT NULL,
    pick INTEGER NOT NULL,
    watermark VARCHAR
);

CREATE TABLE IF NOT EXISTS white_cards (
    id INTEGER PRIMARY KEY,
    text VARCHAR NOT NULL,
    watermark VARCHAR
);

CREATE TABLE IF NOT EXISTS card_set (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS card_set_black_card (
    card_set_id INTEGER NOT NULL,
    black_card_id INTEGER NOT NULL,
    PRIMARY KEY (card_set_id, black_card_id),
    FOREIGN KEY (card_set_id) REFERENCES card_set(id),
    FOREIGN KEY (black_card_id) REFERENCES black_cards(id)
);

CREATE TABLE IF NOT EXISTS card_set_white_card (
    card_set_id INTEGER NOT NULL,
    white_card_id INTEGER NOT NULL,
    PRIMARY KEY (card_set_id, white_card_id),
    FOREIGN KEY (card_set_id) REFERENCES card_set(id),
    FOREIGN KEY (white_card_id) REFERENCES white_cards(id)
);

-- Create user-related tables if they don't exist
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_personalities (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    ai_personality_id INTEGER NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (ai_personality_id) REFERENCES ai_personalities(id)
);

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    game_session_id INTEGER NOT NULL,
    round INTEGER NOT NULL,
    user_score INTEGER NOT NULL,
    ai_score INTEGER NOT NULL,
    FOREIGN KEY (game_session_id) REFERENCES game_sessions(id)
);

-- Indexes for performance (create if they don't exist)
CREATE INDEX IF NOT EXISTS idx_game_sessions_user_id ON game_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_game_sessions_ai_personality_id ON game_sessions(ai_personality_id);
CREATE INDEX IF NOT EXISTS idx_scores_game_session_id ON scores(game_session_id);