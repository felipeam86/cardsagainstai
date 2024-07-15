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
CREATE INDEX IF NOT EXISTS idx_game_sessions_user_id ON game_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_game_sessions_ai_personality_id ON game_sessions(ai_personality_id);

CREATE TABLE IF NOT EXISTS game_rounds (
    id INTEGER PRIMARY KEY,
    game_session_id INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    black_card_id INTEGER NOT NULL,
    user_score INTEGER NOT NULL,
    ai_score INTEGER NOT NULL,
    winner VARCHAR NOT NULL CHECK (winner IN ('user', 'ai')),
    judge_explanation TEXT,
    FOREIGN KEY (game_session_id) REFERENCES game_sessions(id),
    FOREIGN KEY (black_card_id) REFERENCES black_cards(id)
);
CREATE INDEX IF NOT EXISTS idx_game_rounds_game_session_id ON game_rounds(game_session_id);
CREATE INDEX IF NOT EXISTS idx_game_rounds_round_number ON game_rounds(round_number);
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_game_round 
ON game_rounds(game_session_id, round_number);

CREATE TABLE IF NOT EXISTS card_plays (
    id INTEGER PRIMARY KEY,
    round_id INTEGER NOT NULL,
    user_card_id INTEGER NOT NULL,
    ai_card_id INTEGER NOT NULL,
    play_order INTEGER NOT NULL,
    FOREIGN KEY (round_id) REFERENCES game_rounds(id),
    FOREIGN KEY (user_card_id) REFERENCES white_cards(id),
    FOREIGN KEY (ai_card_id) REFERENCES white_cards(id)
);
CREATE INDEX IF NOT EXISTS idx_card_plays_round_id ON card_plays(round_id);
CREATE INDEX IF NOT EXISTS idx_card_plays_user_card_id ON card_plays(user_card_id);
CREATE INDEX IF NOT EXISTS idx_card_plays_ai_card_id ON card_plays(ai_card_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_card_play 
ON card_plays(round_id, play_order);
