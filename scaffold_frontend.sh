#!/bin/bash

# Create root directory
mkdir -p frontend && cd frontend

# Create directory structure
mkdir -p public src/components src/services src/utils src/styles

# Create files
touch public/index.html public/favicon.ico
touch src/components/HomePage.jsx src/components/GamePage.jsx
touch src/services/apiClient.js
touch src/styles/index.css
touch src/App.jsx src/index.js
touch .gitignore package.json README.md tailwind.config.js

# Initialize npm project
npm init -y

# Install dependencies
npm install react react-dom react-scripts axios tailwindcss@latest postcss@latest autoprefixer@latest lucide-react

# Install development dependencies
npm install --save-dev @babel/plugin-proposal-private-property-in-object

# Update package.json scripts
npm pkg set scripts.start="react-scripts start"
npm pkg set scripts.build="react-scripts build"
npm pkg set scripts.test="react-scripts test"
npm pkg set scripts.eject="react-scripts eject"

# Initialize Tailwind CSS
npx tailwindcss init -p

# Add Tailwind directives to src/styles/index.css
echo "@tailwind base;
@tailwind components;
@tailwind utilities;" > src/styles/index.css

# Update .gitignore
echo "node_modules
build
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*" > .gitignore

echo "Frontend project scaffolded successfully!"