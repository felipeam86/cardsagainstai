import React, { useState, useEffect } from 'react';
import { User, Bot, Award, XCircle, Trophy } from 'lucide-react';
import { createGameRound, submitGameRound, endGameSession } from '../services/apiClient';

export default function GamePage({ initialGameData, onReturnHome }) {
  const [gameState, setGameState] = useState(initialGameData);
  const [selectedCards, setSelectedCards] = useState([]);
  const [showJudgeModal, setShowJudgeModal] = useState(false);
  const [showEndGameModal, setShowEndGameModal] = useState(false);
  const [showFinalResultModal, setShowFinalResultModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('Game Page initialized with data:', initialGameData);
  }, [initialGameData]);

  const handleCardSelect = (cardId) => {
    if (selectedCards.includes(cardId)) {
      setSelectedCards(selectedCards.filter(id => id !== cardId));
    } else if (selectedCards.length < gameState.black_card.pick) {
      setSelectedCards([...selectedCards, cardId]);
    }
  };

  const handleSubmitCards = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await submitGameRound(
        gameState.game_round.id, 
        selectedCards, 
        gameState.white_cards.map(card => card.id)
      );
      setGameState(prevState => ({
        ...prevState,
        game_round: response.data.game_round,
        ai_chosen_cards: response.data.ai_chosen_cards
      }));
      setShowJudgeModal(true);
    } catch (error) {
      console.error('Error submitting cards:', error);
      setError('Failed to submit cards. Please try again.');
    }
    setIsLoading(false);
  };

  const handleNextRound = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await createGameRound(gameState.game_round.game_session_id);
      setGameState(response.data);
      setSelectedCards([]);
      setShowJudgeModal(false);
    } catch (error) {
      console.error('Error starting next round:', error);
      setError('Failed to start next round. Please try again.');
    }
    setIsLoading(false);
  };

  const handleEndGame = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await endGameSession(gameState.game_round.game_session_id);
      setGameState(prevState => ({
        ...prevState,
        final_result: response.data
      }));
      setShowEndGameModal(false);
      setShowFinalResultModal(true);
    } catch (error) {
      console.error('Error ending game:', error);
      setError('Failed to end the game. Please try again.');
    }
    setIsLoading(false);
  };

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left column - Black card */}
      <div className="w-1/5 bg-black p-4 flex flex-col">
        <h1 className="text-xl font-bold text-white mb-4">Cards Against AI</h1>
        
        <div className="bg-gray-800 rounded-lg p-4 flex-grow flex flex-col justify-between">
          <p className="text-white text-xl font-bold">{gameState.black_card.text}</p>
          <div className="self-end text-right">
            <p className="text-gray-400 text-sm mb-1">Pick: {gameState.black_card.pick}</p>
            <p className="text-gray-400 text-xs">Cards Against Humanity</p>
          </div>
        </div>
      </div>
      
      {/* Middle column - White cards */}
      <div className="w-3/5 bg-gray-200 p-4 overflow-y-auto">
        <div className="grid grid-cols-3 gap-3">
          {gameState.white_cards.map((card) => (
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
                <span className="text-white">You: {gameState.game_round.user_score}</span>
              </div>
              <div className="flex items-center">
                <Bot className="text-white mr-2" size={18} />
                <span className="text-white">AI: {gameState.game_round.ai_score}</span>
              </div>
              <div className="flex items-center">
                <Award className="text-white mr-2" size={18} />
                <span className="text-white">Round: {gameState.game_round.round_number}</span>
              </div>
            </div>
          </div>

          {/* Submit button */}
          <button
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={handleSubmitCards}
            disabled={isLoading || selectedCards.length !== gameState.black_card.pick}
          >
            {isLoading ? 'Submitting...' : `Submit Cards (${selectedCards.length}/${gameState.black_card.pick})`}
          </button>
        </div>

        {/* End Game button */}
        <button
          onClick={() => setShowEndGameModal(true)}
          className="w-full px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 flex items-center justify-center"
        >
          <XCircle className="mr-2" size={18} />
          End Game
        </button>
      </div>

      {/* Judge Decision Modal */}
      {showJudgeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-4xl w-full">
            <h2 className="text-2xl font-bold mb-4">Judge's Decision</h2>
            <div className="mb-4">
              <p className="text-lg font-semibold mb-2">Black Card:</p>
              <div className="bg-gray-800 text-white p-3 rounded flex flex-col justify-between min-h-[8rem]">
                <p className="text-xl">{gameState.black_card.text}</p>
                <div className="self-end text-right">
                  <p className="text-gray-400 text-sm mb-1">Pick: {gameState.black_card.pick}</p>
                  <p className="text-gray-400 text-xs">Cards Against Humanity</p>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-lg font-semibold mb-2">Your Play:</p>
                <div className="space-y-2">
                  {selectedCards.map(id => {
                    const card = gameState.white_cards.find(card => card.id === id);
                    return (
                      <div key={id} className="bg-blue-100 p-3 rounded min-h-[8rem] flex flex-col justify-between">
                        <p className="text-sm">{card?.text}</p>
                        <p className="text-xs text-gray-500 self-end">Cards Against Humanity</p>
                      </div>
                    );
                  })}
                </div>
              </div>
              <div>
                <p className="text-lg font-semibold mb-2">AI's Play:</p>
                <div className="space-y-2">
                  {gameState.ai_chosen_cards.map(card => (
                    <div key={card.id} className="bg-red-100 p-3 rounded min-h-[8rem] flex flex-col justify-between">
                      <p className="text-sm">{card.text}</p>
                      <p className="text-xs text-gray-500 self-end">Cards Against Humanity</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="mb-4">
              <p className="text-lg font-semibold mb-2">Winner: {gameState.game_round.winner === 'human' ? 'You!' : 'AI'}</p>
              <p className="italic">{gameState.game_round.judge_explanation}</p>
            </div>
            <button
              className="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              onClick={handleNextRound}
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
                onClick={handleEndGame}
              >
                End Game
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Final Result Modal */}
      {showFinalResultModal && gameState.final_result && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <Trophy className="text-yellow-500 mr-2" size={24} />
              Final Results
            </h2>
            <div className="mb-6 space-y-2">
              <p className="text-lg">
                <span className="font-semibold">Your Score:</span> {gameState.final_result.user_score}
              </p>
              <p className="text-lg">
                <span className="font-semibold">AI Score:</span> {gameState.final_result.ai_score}
              </p>
              <p className="text-lg">
                <span className="font-semibold">Rounds Played:</span> {gameState.final_result.rounds_played}
              </p>
              <p className="text-xl font-bold mt-4">
                Winner: {gameState.final_result.winner === 'human' ? 'You!' : 'AI'}
              </p>
            </div>
            <div className="flex justify-end space-x-4">
              <button
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                onClick={() => {
                  // Reset game state and start a new game
                  setGameState(initialGameData);
                  setSelectedCards([]);
                  setShowFinalResultModal(false);
                }}
              >
                Play Again
              </button>
              <button
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                onClick={onReturnHome}
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