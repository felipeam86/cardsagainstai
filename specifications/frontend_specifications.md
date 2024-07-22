# Cards Against AI - Front-end Specifications

## Overview
Cards Against AI is a web-based game inspired by Cards Against Humanity, featuring a single human player competing against an AI opponent. The game consists of two main screens: a home page for user creation and AI opponent selection, and the main game interface.

## Technology Stack
- Frontend: React
- Styling: Tailwind CSS
- Icons: Lucide React

## Application Structure
1. Main Component (CardsAgainstAIMain)
2. Home Page (HomePage)
3. Game Page (CardAgainstAIGame)

## Detailed Component Specifications

### 1. Main Component (CardsAgainstAIMain)
- Manages the state of whether the game has started
- Handles the flow between the Home Page and the Game Page
- Passes the selected AI opponent and username to the Game Page

### 2. Home Page (HomePage)
#### Layout
- Centered content with a maximum width of 384px (w-96)
- White background with rounded corners and shadow

#### Features
- Game title: "Cards Against AI"
- Username input field
- AI opponent selection dropdown
- "Add Custom AI" button
- Custom AI name and description input field (appears when "Add Custom AI" is clicked)
- "Start Game" button (enabled only when a username is entered and an AI is selected)

#### Functionality
- Allows users to enter a username for the game session
- Allows selection of pre-defined AI opponents
- Enables creation of custom AI opponents
- Starts the game with the entered username and selected AI opponent

#### User Management
- Users claim a username for each game session
- No authentication required; usernames are session-based
- Implement client-side validation for username (e.g., non-empty, max length)
- Store username in component state and pass it to the game page when starting a game

### 3. Game Page (CardAgainstAIGame)
#### Layout
- Vertical split design
  - Left side (1/3 width): Black background, contains black card and scores
  - Right side (2/3 width): Light gray background, contains the hand of 10 white cards

#### Left Side Components
- Game title: "Cards Against AI"
- Black card display
  - Dark gray background
  - White text
  - "Pick: X cards" displayed in bottom left
  - Watermark in bottom right
- Score display
  - Shows player score, AI score, and current round
  - Uses icons for visual representation (User, Bot, Award)
- Round counter to track the current round
- Final results display showing the overall winner and final scores

#### Right Side Components
- Grid display of white cards (3 columns)
- Card selection counter
- "Submit Cards" button
- "End Game" button

#### White Card Design
- White background with rounded corners and shadow
- Text left-justified at the top
- Watermark in bottom right
- Blue ring around selected cards

#### Judge Decision Modal
- Appears after cards are submitted
- Full-screen overlay with semi-transparent black background
- Modal content:
  - White background with rounded corners and shadow
  - Displays the black card at the top
  - Shows both the player's and AI's selected white cards side by side
  - Highlights the winning combination with a colored background and border
    - Green for player win
    - Blue for AI win
  - Judge's explanation of the winning combination
  - "Next Round" button

#### Final Results Modal
- Appears when user hits "End Game" button.
- Displays the final scores for both the player and the AI
- Announces the overall winner
- Provides options to:
  - Play Again (starts a new game with the same AI opponent)
  - Change AI Opponent (returns to the home page)

## Gameplay Flow
1. User enters a username and selects or creates an AI opponent on the Home Page
2. User clicks "Start Game" button
3. Once in the game, black card and the 10 white card hand are displayed for the round
4. Player selects the required number of white cards
5. Player submits their selection
6. Backend responds with game round results and ai chosen cards.
7. Judge Decision Modal appears with both player's and AI's selections, highlighting the winner
8. Steps 3-7 repeat until user hits "End Game" button
9. Display the final game results, including scores and the winner

## Error Handling and Game Termination

### Error Display
1. Create a simple Error Modal component for displaying Anthropic API errors.
2. The Error Modal should include:
   - A hazard icon (e.g., exclamation triangle)
   - An apology message
   - A "Return to Home" button

### Error Scenario
1. Anthropic API Errors:
   - Display the Error Modal when unable to communicate with the Anthropic API
   - End the game and return to the home screen when the user acknowledges the error

## Design Principles
- High contrast between black and white elements
- Simple color scheme: black, white, shades of gray, with blue and green accents
- Responsive layout adaptable to different screen sizes
- Use of icons for visual representation of game elements
- Clear visual feedback for user interactions (username entry, card selection, button states)
- Simple and informative error messages for user limit and other error scenarios

## Accessibility Considerations
- Ensure sufficient color contrast for text readability
- Provide alt text for all icons and images
- Implement keyboard navigation for form inputs, card selection, and button interactions
- Ensure error modals are accessible to screen readers

## Future Enhancements (not implemented in current design)
- Animations for card selection and modal appearances
- Sound effects for various game actions
- Expanded statistics and game history tracking
- Multiplayer functionality

## Development Notes
- Implement proper state management for game sessions and progression
- Ensure responsive design works across various device sizes
- Implement actual game logic for AI opponent behavior and judging
- Create reusable components for cards to maintain consistency
- Consider implementing a custom hook for card selection logic
- Ensure smooth transitions when showing and hiding the judge decision modal
- Ensure proper error handling for network requests, including user limit checks

This summary provides a comprehensive overview of the design decisions for the Cards Against AI game, including the updated home page with user management. It covers the overall structure, detailed component specifications, gameplay flow, and design principles. The front-end developer should use this as a guide for implementing the user interface and interactions of the game.