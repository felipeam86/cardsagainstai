#!/bin/bash

# Create the frontend directory
mkdir frontend
cd frontend

# Initialize Next.js project
npx create-next-app@latest . --use-npm --typescript --eslint --tailwind --app --src-dir --import-alias "@/*"

# Create additional directories
mkdir -p components hooks store utils

# Create component files
touch components/HomePage.tsx components/GamePage.tsx components/BlackCard.tsx components/WhiteCard.tsx components/ScoreBoard.tsx components/JudgeDecisionModal.tsx components/FinalResultsModal.tsx

# Create hook file
touch hooks/useGame.ts

# Create store file
touch store/gameStore.ts

# Create utility file
touch utils/api.ts

# Install additional dependencies
npm install zustand @tanstack/react-query @tanstack/react-query-devtools

# Update package.json scripts
sed -i '' 's/"dev": "next dev"/"dev": "next dev -p 3000"/' package.json

echo "Frontend project scaffold complete!"