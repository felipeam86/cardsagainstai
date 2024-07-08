# Cards Against AI - Front end specifications

## Overview
Cards Against AI is a web-based game inspired by Cards Against Humanity, featuring a single human player competing against an AI opponent. The game consists of two main screens: a home page for AI opponent selection and the main game interface.

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
- Passes the selected AI opponent to the Game Page

### 2. Home Page (HomePage)
#### Layout
- Centered content with a maximum width of 384px (w-96)
- White background with rounded corners and shadow

#### Features
- Game title: "Cards Against AI"
- AI opponent selection dropdown
- "Add Custom AI" button
- Custom AI name input field (appears when "Add Custom AI" is clicked)
- "Start Game" button (enabled only when an AI is selected)

#### Functionality
- Allows selection of pre-defined AI opponents
- Enables creation of custom AI opponents
- Starts the game with the selected AI opponent

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
1. Player selects or creates an AI opponent on the Home Page
2. Game starts with the selected AI opponent
3. Black card is displayed for the round
4. Player selects the required number of white cards
5. Player submits their selection
6. Judge Decision Modal appears with both player's and AI's selections, highlighting the winner
7. Player can share the result or proceed to the next round

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
- Simple color scheme: black, white, shades of gray, with blue and green accents for highlighting
- Responsive layout adaptable to different screen sizes
- Use of icons for visual representation of game elements
- Clear visual feedback for card selection and round results

## Accessibility Considerations
- Ensure sufficient color contrast for text readability
- Provide alt text for all icons and images
- Implement keyboard navigation for card selection and button interactions

## Future Enhancements (not implemented in current design)
- Animations for card selection and modal appearances
- Sound effects for various game actions
- Expanded statistics and game history tracking
- Multiplayer functionality

## Development Notes
- Implement proper state management for game progression
- Ensure responsive design works across various device sizes
- Implement actual game logic for AI opponent behavior and judging
- Create reusable components for cards to maintain consistency
- Implement actual social sharing functionality
- Consider implementing a custom hook for card selection logic
- Ensure smooth transitions when showing and hiding the judge decision modal

This summary provides a comprehensive overview of the design decisions for the Cards Against AI game. It covers the overall structure, detailed component specifications, gameplay flow, and design principles. The front-end developer should use this as a guide for implementing the user interface and interactions of the game.