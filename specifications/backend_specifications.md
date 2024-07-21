# Cards Against AI - Backend Specification

## 1. Overview

Cards Against AI is a web-based game inspired by Cards Against Humanity, featuring a single human player competing against an AI opponent. This document outlines the backend architecture and specifications for implementing the game server.

## 2. Architecture

The backend is built using Python 3.10 with FastAPI framework utilizing SQLite for data persistence. The AI opponent and judge functionality are powered by the Anthropic API (Claude 3.5 Sonnet model).

### Key Components:

1. FastAPI Backend
2. SQLite Database
3. Anthropic API Integration
4. Game State Manager
5. Card Manager

## 3. Data Model

The data model is based on the provided SQLite schema, which includes tables for black cards, white cards, game sessions, game rounds, and AI personalities.

### Key Entities:
- User: Represents a player in the game.
- AIPersonality: Represents an AI opponent personality that can be selected for a game.
- GameSession: Represents a single game session between a user and an AI opponent.
- GameRound: Represents a single round within a game session.
- BlackCard, WhiteCard: Represent the game cards.

## 4. Game Logic

### User Sessions:
- Sessions last as long as the browser tab is open
- No authentication required; users claim a username for the session duration
- Use game session ID as the unique identifier of the game
- Allow multiple game sessions to be played simultaneously with the same username

### Card Management:
- Both the user and AI opponent draw from the same card pool
- Ensure fair and random distribution of cards to both the user and AI opponent

### Game Flow:
1. User creates a game session by selecting an AI opponent personality.
2. Game starts with a random draw of the same 10 cards hand for both the user and AI opponent.
3. For each round (total of 10 rounds):
   a. Display a black card and draw 10 random cards hand.
   b. User selects white card(s) from the hand
   c. When the user hits submit, the AI opponent selects white card(s) from the same hand using the Anthropic API
   d. User and AI selections are submitted to the judge (Anthropic API)
   e. Determine round winner and update scores (the winner of a round gets one point)
   g. Record round history and start a new round
4. The game ends when the user hits the 'End game' button.


## 5. Anthropic API Integration

The Anthropic API is used for:
- AI opponent: Selecting white cards to play in response to black cards
- Judge functionality: Determining the winner of each round and providing an explanation

The AI opponent logic is based on a prompt that includes:
- The black card
- The cards available to be played
- The AI personality
- A request to choose the funniest card(s)

The AI judge logic is based on a prompt that includes:
- The black card
- Cards played by the human and ai opponent
- A request to choose who proposed the funniest card

Retry mechanism: Implement up to 3 retry attempts for API calls, with exponential backoff.
Error handling: If persistent issues occur after retries, gracefully end the game and inform the user.


## 6. Implementation Guidelines

### Technology Stack:
- Backend: Python 3.10 with FastAPI
- Database: SQLite with SQLModel ORM
- API Integration: Anthropic API client

### Project Structure:
```
backend/
├── app/
│   ├── main.py
│   ├── dependencies.py
│   ├── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── database.py
│   └── services/
│       ├── __init__.py
│       ├── anthropic.py
│       ├── game.py
│       └── card_manager.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_game_sessions.py
│   │   ├── test_game_rounds.py
│   │   └── test_ai_personalities.py
│   └── test_services/
│       ├── __init__.py
│       ├── test_anthropic.py
│       ├── test_game.py
│       └── test_card_manager.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
├── .env
├── .gitignore
└── README.md
```

### Development Process:
1. Set up the FastAPI application with the proposed structure
2. Implement SQLAlchemy models based on the provided schema
3. Create API routes and implement game logic in the service layer
4. Integrate with the Anthropic API for AI opponent and judge functionality
5. Set up Docker and Docker Compose for containerization
6. Write unit and integration tests
7. Create a Makefile with commands for running the application, tests, and other common tasks
8. Document the setup and running process in the README.md file

## 7. Error Handling and Logging
- Implement comprehensive error handling throughout the application
- Use Python's built-in logging module for application logging
- Log all significant events, errors, and API interactions

### Testing:
- Implement unit tests for individual components and functions
- Create integration tests for API endpoints and game flow
- Use pytest as the testing framework

### Documentation:
- Provide inline documentation for all significant functions and classes
- Create API documentation using FastAPI's built-in Swagger UI

## 8. Deployment

Use Docker and Docker Compose for containerization and easy deployment. The Dockerfile and docker-compose.yml files should be configured to set up the entire application stack, including the FastAPI server, and SQLite database.


## 9. Conclusion

This specification provides a comprehensive guide for implementing the Cards Against AI backend using Python 3.10. The developer should adhere to Python 3.10 best practices, follow the FastAPI documentation for implementation details, and ensure robust error handling and testing throughout the development process.