#!/bin/bash

# Create main directory structure
mkdir -p backend/app/{api/endpoints,core,db,services,utils}
mkdir -p backend/tests/{test_api,test_services}

# Create main application files
touch backend/app/main.py
touch backend/app/api/__init__.py
touch backend/app/api/dependencies.py

# Create API endpoint files
touch backend/app/api/endpoints/{__init__,users,game_sessions,game_rounds,ai_personalities,status}.py

# Create core files
touch backend/app/core/{__init__,config,security}.py

# Create database files
touch backend/app/db/{__init__,models,database}.py

# Create service files
touch backend/app/services/{__init__,anthropic,game,card_manager,redis_manager}.py

# Create utility files
touch backend/app/utils/{__init__,logging}.py

# Create test files
touch backend/tests/{__init__,conftest}.py
touch backend/tests/test_api/{__init__,test_users,test_game_sessions,test_game_rounds,test_ai_personalities}.py
touch backend/tests/test_services/{__init__,test_anthropic,test_game,test_card_manager,test_redis_manager}.py

# Create root level files
touch backend/{Dockerfile,docker-compose.yml,requirements.txt,Makefile,.env,.gitignore,README.md}

echo "Project structure created successfully!"