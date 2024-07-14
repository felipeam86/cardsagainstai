# Cards Against AI - Backend Specification

## 1. Overview

Cards Against AI is a web-based game inspired by Cards Against Humanity, featuring a single human player competing against an AI opponent. This document outlines the backend architecture and specifications for implementing the game server.

## 2. Architecture

The backend is built using Python 3.10 with FastAPI framework, utilizing SQLite for data persistence and Redis for caching and game state management. The AI opponent and judge functionality are powered by the Anthropic API (Claude Haiku model).

### Key Components:

1. FastAPI Backend
2. SQLite Database
3. Redis Cache
4. Anthropic API Integration
5. Game State Manager
6. User Session Manager
7. Card Manager
8. Game History Manager

## 3. Data Model

The data model is based on the provided SQLite schema, which includes tables for black cards, white cards, card sets, and their relationships. Additional tables have been implemented for user sessions, game sessions, game rounds, and AI personalities.

### Key Entities:
- User: Represents a player in the game.
- AIPersonality: Represents an AI opponent personality that can be selected for a game.
- GameSession: Represents a single game session between a user and an AI opponent.
- GameRound: Represents a single round within a game session.
- BlackCard, WhiteCard: Represent the game cards.
- CardSet: Represents a set of cards that can be used in the game.

## 4. API Endpoints

### User Management:
- POST /users: Create a new user session
- DELETE /users/{user_id}: End a user session

### Game Management:
- POST /game-sessions: Create a new game session
- GET /game-sessions/{session_id}: Get game session state
- POST /game-sessions/{session_id}/start: Start the game session
- POST /game-rounds/{round_id}/submit: Submit card(s) for a round
- GET /game-rounds/{round_id}/result: Get round result

### Card Management:
- GET /cards/black: Get a new black card
- GET /cards/white: Get white cards for a player
- GET /card-sets: Get all available card sets

### Game History:
- GET /history/{user_id}: Get game history for a user

### Server Status:
- GET /status: Check server capacity

### AI Personalities:
- GET /ai-personalities: Fetch available AI personalities
- POST /ai-personalities: Create a new AI personality

### Score Management
   - GET /games/{game_id}/scores: Retrieve current game scores
   - POST /games/{game_id}/scores: Update scores after a round

### Game Completion
   - POST /games/{game_id}/complete: Finalize a game

### Social Sharing: To align with frontend specifications, add:
   - POST /games/{game_id}/share: Generate shareable content for social media

## 5. Game Logic

### User Sessions:
- Sessions last as long as the browser tab is open
- No authentication required; users claim a username for the session duration
- Use Redis to track active sessions and enforce the 100-user limit

### Card Management:
- Implement a system to track which cards remain in the deck using Redis
- Both the user and AI opponent draw from the same card pool
- Cards drawn by either the user or AI are removed from the game deck
- Played cards do not return to the deck during the game session
- Ensure fair and random distribution of cards to both the user and AI opponent

### Game Flow:
1. User creates a game session by selecting an AI opponent personality.
2. Game starts with drawing initial hands for both the user and AI opponent from the same deck.
3. For each round (total of 10 rounds):
   a. Display a black card
   b. User selects white card(s) from their hand
   c. AI opponent selects white card(s) using the Anthropic API
   d. Submit selections to the judge (Anthropic API)
   e. Determine round winner and update scores
   f. Replenish hands by drawing new white cards from the remaining deck
   g. Record round history
4. After 10 rounds, determine the game winner
   - If there's a tie, an extra tiebreaker round is played
5. Save detailed game history


## 6. Redis Integration

Redis is used for:
- Storing active game states, including current round, scores, and game status
- Managing active user sessions
- Implementing the 100-user limit

Game state in Redis is structured as a hash with the game session ID as the key, containing fields for status, current round, and scores.


## 7. Anthropic API Integration

The Anthropic API is used for:
- AI opponent: Selecting white cards to play in response to black cards
- Judge functionality: Determining the winner of each round and providing an explanation

Retry mechanism: Implement up to 3 retry attempts for API calls, with exponential backoff.
Error handling: If persistent issues occur after retries, gracefully end the game and inform the user.


## 8. Implementation Guidelines

### Technology Stack:
- Backend: Python 3.10 with FastAPI
- Database: SQLite with SQLAlchemy ORM
- Caching and State Management: Redis
- API Integration: Anthropic API client

### Project Structure:
```
cards_against_ai/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── routes/
│   │   ├── models/
│   │   └── schemas/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── services/
│   │   ├── anthropic.py
│   │   ├── game_state.py
│   │   ├── card_manager.py
│   │   ├── history_manager.py
│   │   ├── redis_manager.py
│   │   └── ai_personality_manager.py
│   └── utils/
│       └── logging.py
├── tests/
├── alembic/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
└── README.md
```

### Development Process:
1. Set up the FastAPI application with the proposed structure
2. Implement SQLAlchemy models based on the provided schema
3. Set up Redis connection and create a Redis manager service
4. Create API routes and implement game logic in the service layer
5. Integrate with the Anthropic API for AI opponent and judge functionality
6. Implement Redis-based caching for game state management
7. Set up Docker and Docker Compose for containerization (including Redis)
8. Write unit and integration tests
9. Create a Makefile with commands for running the application, tests, and other common tasks
10. Document the setup and running process in the README.md file

### Error Handling and Logging:
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

## 9. Deployment

Use Docker and Docker Compose for containerization and easy deployment. The Dockerfile and docker-compose.yml files should be configured to set up the entire application stack, including the FastAPI server, SQLite database, and Redis instance.

Example docker-compose.yml structure:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379

  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"
```

Ensure that the Dockerfile uses Python 3.10 as the base image.

## 10. Conclusion

This specification provides a comprehensive guide for implementing the Cards Against AI backend using Python 3.10 and Redis for caching and state management. The developer should adhere to Python 3.10 best practices, leverage Redis for efficient data caching and real-time operations, follow the FastAPI documentation for implementation details, and ensure robust error handling and testing throughout the development process.