import React, { useState } from 'react';
import { User, Bot, Award, XCircle, Trophy } from 'lucide-react';

export default function GamePage() {
  const [selectedCards, setSelectedCards] = useState([]);
  const [showJudgeModal, setShowJudgeModal] = useState(false);
  const [showEndGameModal, setShowEndGameModal] = useState(false);
  const [showFinalResultModal, setShowFinalResultModal] = useState(false);
  
  // Mock game state (in a real app, this would be managed by your game logic)
  const [gameState, setGameState] = useState({
    userScore: 3,
    aiScore: 2,
    roundsPlayed: 5
  });

  const blackCard = {
    text: "Why can't I sleep at night?",
    pick: 1,
  };

  const whiteCards = [
    { id: 1, text: "Aliens probing my brain with their advanced technology while I'm trying to count sheep." },
    { id: 2, text: "Crippling debt that's slowly consuming my soul and my savings account." },
    { id: 3, text: "A tiny horse galloping through my dreams, leaving hoof prints on my subconscious." },
    { id: 4, text: "Existential dread creeping in as I contemplate the vastness of the universe and my insignificance." },
    { id: 5, text: "My extensive collection of high-tech sex toys humming ominously in the closet." },
    { id: 6, text: "The entire cast of Downton Abbey having a tea party in my bedroom." },
    { id: 7, text: "A really cool hat that whispers secrets of the universe when I wear it to bed." },
    { id: 8, text: "Nicolas Cage reciting the Declaration of Independence in increasingly hysterical tones." },
    { id: 9, text: "The unstoppable march of time reminding me of my own mortality with each tick of the clock." },
    { id: 10, text: "A subscription box of gross snacks that arrived today, tempting me with its weird flavors." },
  ];

  const handleCardSelect = (cardId) => {
    if (selectedCards.includes(cardId)) {
      setSelectedCards(selectedCards.filter(id => id !== cardId));
    } else if (selectedCards.length < blackCard.pick) {
      setSelectedCards([...selectedCards, cardId]);
    }
  };

  const handleEndGameClick = () => {
    setShowEndGameModal(true);
  };

  const handleConfirmEndGame = () => {
    setShowEndGameModal(false);
    setShowFinalResultModal(true);
  };

  const handlePlayAgain = () => {
    // Reset game state here
    setShowFinalResultModal(false);
    // Additional logic to start a new game
  };

  const handleReturnHome = () => {
    // Logic to return to home screen
    setShowFinalResultModal(false);
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left column - Black card */}
      <div className="w-1/5 bg-black p-4 flex flex-col">
        <h1 className="text-xl font-bold text-white mb-4">Cards Against AI</h1>
        
        <div className="bg-gray-800 rounded-lg p-4 flex-grow flex flex-col justify-between">
          <p className="text-white text-xl font-bold">{blackCard.text}</p>
          <div className="self-end text-right">
            <p className="text-gray-400 text-sm mb-1">Pick: {blackCard.pick}</p>
            <p className="text-gray-400 text-xs">Cards Against Humanity</p>
          </div>
        </div>
      </div>
      
      {/* Middle column - White cards */}
      <div className="w-3/5 bg-gray-200 p-4 overflow-y-auto">
        <div className="grid grid-cols-3 gap-3">
          {whiteCards.map((card) => (
            <div
              key={card.id}
              className={`bg-white p-3 rounded-lg shadow cursor-pointer transition-all duration-200 h-40 flex flex-col justify-between ${
                selectedCards.includes(card.id) ? 'ring-2 ring-blue-500 transform scale-105' : 'hover:shadow-lg'
              }`}
              onClick={() => handleCardSelect(card.id)}
            >
              <p className="text-xs font-semibold leading-tight">{card.text}</p>
              <div className="self-end text-right">
                <p className="text-gray-400 text-xxs">Cards Against Humanity</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Right column - Score, Submit, End Game */}
      <div className="w-1/5 bg-gray-300 p-4 flex flex-col justify-between">
        <div>
          {/* Score card */}
          <div className="bg-gray-900 rounded-lg p-4 mb-4">
            <div className="flex flex-col items-start space-y-2">
              <div className="flex items-center">
                <User className="text-white mr-2" size={18} />
                <span className="text-white">You: {gameState.userScore}</span>
              </div>
              <div className="flex items-center">
                <Bot className="text-white mr-2" size={18} />
                <span className="text-white">AI: {gameState.aiScore}</span>
              </div>
              <div className="flex items-center">
                <Award className="text-white mr-2" size={18} />
                <span className="text-white">Round: {gameState.roundsPlayed}</span>
              </div>
            </div>
          </div>

          {/* Submit button */}
          <button
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => setShowJudgeModal(true)}
            disabled={selectedCards.length !== blackCard.pick}
          >
            Submit Cards ({selectedCards.length}/{blackCard.pick})
          </button>
        </div>

        {/* End Game button */}
        <button
          onClick={handleEndGameClick}
          className="w-full px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 flex items-center justify-center"
        >
          <XCircle className="mr-2" size={18} />
          End Game
        </button>
      </div>

      {/* Judge Decision Modal */}
      {showJudgeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full">
            <h2 className="text-2xl font-bold mb-4">Judge's Decision</h2>
            <div className="mb-4">
              <p className="text-lg font-semibold mb-2">Black Card:</p>
              <div className="bg-gray-800 text-white p-3 rounded flex flex-col justify-between h-32">
                <p className="text-xl">{blackCard.text}</p>
                <div className="self-end text-right">
                  <p className="text-gray-400 text-sm mb-1">Pick: {blackCard.pick}</p>
                  <p className="text-gray-400 text-xs">Cards Against Humanity</p>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-lg font-semibold mb-2">Your Play:</p>
                <div className="bg-blue-100 p-3 rounded h-32 flex flex-col justify-between">
                  <p className="text-sm">{whiteCards.find(card => card.id === selectedCards[0])?.text}</p>
                  <p className="text-xs text-gray-500 self-end">Cards Against Humanity</p>
                </div>
              </div>
              <div>
                <p className="text-lg font-semibold mb-2">AI's Play:</p>
                <div className="bg-red-100 p-3 rounded h-32 flex flex-col justify-between">
                  <p className="text-sm">{whiteCards[Math.floor(Math.random() * whiteCards.length)].text}</p>
                  <p className="text-xs text-gray-500 self-end">Cards Against Humanity</p>
                </div>
              </div>
            </div>
            <div className="mb-4">
              <p className="text-lg font-semibold mb-2">Winner: You!</p>
              <p className="italic">"Your answer was hilariously on point. The AI needs to step up its game!"</p>
            </div>
            <button
              className="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              onClick={() => setShowJudgeModal(false)}
            >
              Next Round
            </button>
          </div>
        </div>
      )}

      {/* End Game Modal */}
      {showEndGameModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">End Game</h2>
            <p className="mb-4">Are you sure you want to end the game?</p>
            <div className="flex justify-end space-x-4">
              <button
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                onClick={() => setShowEndGameModal(false)}
              >
                Cancel
              </button>
              <button
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                onClick={handleConfirmEndGame}
              >
                End Game
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Final Result Modal */}
      {showFinalResultModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <Trophy className="text-yellow-500 mr-2" size={24} />
              Final Results
            </h2>
            <div className="mb-6 space-y-2">
              <p className="text-lg">
                <span className="font-semibold">Your Score:</span> {gameState.userScore}
              </p>
              <p className="text-lg">
                <span className="font-semibold">AI Score:</span> {gameState.aiScore}
              </p>
              <p className="text-lg">
                <span className="font-semibold">Rounds Played:</span> {gameState.roundsPlayed}
              </p>
              <p className="text-xl font-bold mt-4">
                Winner: {gameState.userScore > gameState.aiScore ? 'You!' : 'AI'}
              </p>
            </div>
            <div className="flex justify-end space-x-4">
              <button
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                onClick={handlePlayAgain}
              >
                Play Again
              </button>
              <button
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                onClick={handleReturnHome}
              >
                Return to Home
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
