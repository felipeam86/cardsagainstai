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
- Custom AI name input field (appears when "Add Custom AI" is clicked)
- "Start Game" button (enabled only when a username is entered and an AI is selected)
- Error modal for user limit handling

#### Functionality
- Allows users to enter a username for the game session
- Allows selection of pre-defined AI opponents
- Enables creation of custom AI opponents
- Starts the game with the entered username and selected AI opponent
- Checks for user limit before starting the game
- Displays an error modal if the user limit is reached

#### User Management
- Users claim a username for each game session
- No authentication required; usernames are session-based
- Implement client-side validation for username (e.g., non-empty, max length)
- Store username in component state and pass it to the game page when starting a game

#### User Limit Handling
- Before starting a game, check if the maximum user limit (100) has been reached
- If the limit is reached, display an error modal with the following content:
  - Title: "Unable to Start Game"
  - Message: "We're sorry, but the maximum number of users are currently playing. Please try again later."
  - Close button to dismiss the modal
- The user limit is a hard cap configured through environment variables on the server
- No queue system or wait time estimates are implemented; users are simply asked to try again later

### 3. Game Page (CardAgainstAIGame)
#### Layout
- Vertical split design
  - Left side (1/3 width): Black background, contains black card and scores
  - Right side (2/3 width): Light gray background, contains white cards

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

#### Right Side Components
- Grid display of white cards (3 columns)
- Card selection counter
- "Submit Cards" button

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
  - Social sharing buttons (Twitter, Facebook, LinkedIn)
  - "Next Round" button

## Gameplay Flow
1. User enters a username and selects or creates an AI opponent on the Home Page
2. User clicks "Start Game" button
3. System checks if the user limit has been reached
   - If limit is not reached, game starts with the entered username and selected AI opponent
   - If limit is reached, an error modal is displayed, and the user remains on the Home Page
4. Once in the game, black card is displayed for the round
5. Player selects the required number of white cards
6. Player submits their selection
7. Judge Decision Modal appears with both player's and AI's selections, highlighting the winner
8. Player can share the result or proceed to the next round

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
- Implement proper state management for user sessions and game progression
- Ensure responsive design works across various device sizes
- Implement actual game logic for AI opponent behavior and judging
- Create reusable components for cards to maintain consistency
- Implement actual social sharing functionality
- Consider implementing a custom hook for card selection logic
- Ensure smooth transitions when showing and hiding the judge decision modal
- Implement server-side check for user limit before starting each game session
- Ensure proper error handling for network requests, including user limit checks

This summary provides a comprehensive overview of the design decisions for the Cards Against AI game, including the updated home page with user management and user limit handling. It covers the overall structure, detailed component specifications, gameplay flow, and design principles. The front-end developer should use this as a guide for implementing the user interface and interactions of the game.