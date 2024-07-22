import React, { useState, useEffect } from 'react';
import { PlusCircle, User, Bot } from 'lucide-react';
import { fetchAIPersonalities, createAIPersonality, createGameSession, createGameRound } from '../services/apiClient';

export default function HomePage({ onGameStart }) {
  const [username, setUsername] = useState('');
  const [selectedAI, setSelectedAI] = useState('');
  const [showCustomAI, setShowCustomAI] = useState(false);
  const [customAIName, setCustomAIName] = useState('');
  const [customAIDescription, setCustomAIDescription] = useState('');
  const [aiOpponents, setAiOpponents] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAIPersonalities()
      .then(response => setAiOpponents(response.data))
      .catch(error => setError('Failed to fetch AI opponents'));
  }, []);

  const handleStartGame = async () => {
    setIsLoading(true);
    setError(null);
    try {
      let aiPersonalityId = selectedAI;
      if (showCustomAI) {
        const customAIResponse = await createAIPersonality(customAIName, customAIDescription);
        aiPersonalityId = customAIResponse.data.id;
      }
      const sessionResponse = await createGameSession(username, aiPersonalityId);
      const gameSessionId = sessionResponse.data.id;
      const roundResponse = await createGameRound(gameSessionId);
      onGameStart(roundResponse.data);
    } catch (error) {
      console.error('Error starting game:', error);
      setError('Failed to start the game. Please try again.');
    }
    setIsLoading(false);
  };

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-96 p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-3xl font-bold text-center mb-6">Cards Against AI</h1>
        
        <div className="mb-4">
          <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
            Username
          </label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="pl-10 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your username"
            />
          </div>
        </div>

        <div className="mb-4">
          <label htmlFor="ai-opponent" className="block text-sm font-medium text-gray-700 mb-1">
            Select AI Opponent
          </label>
          <div className="relative">
            <Bot className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
            <select
              id="ai-opponent"
              value={selectedAI}
              onChange={(e) => setSelectedAI(e.target.value)}
              className="pl-10 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select an AI opponent</option>
              {aiOpponents.map((ai) => (
                <option key={ai.id} value={ai.id}>
                  {ai.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button
          onClick={() => setShowCustomAI(!showCustomAI)}
          className="flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-blue-600 bg-blue-100 rounded-md hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
        >
          <PlusCircle className="mr-2" size={18} />
          Add Custom AI
        </button>

        {showCustomAI && (
          <>
            <div className="mb-4">
              <label htmlFor="custom-ai-name" className="block text-sm font-medium text-gray-700 mb-1">
                Custom AI Name
              </label>
              <input
                id="custom-ai-name"
                type="text"
                value={customAIName}
                onChange={(e) => setCustomAIName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter custom AI name"
              />
            </div>
            <div className="mb-4">
              <label htmlFor="custom-ai-description" className="block text-sm font-medium text-gray-700 mb-1">
                Custom AI Description
              </label>
              <textarea
                id="custom-ai-description"
                value={customAIDescription}
                onChange={(e) => setCustomAIDescription(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Describe your custom AI"
                rows={3}
              />
            </div>
          </>
        )}

        <button
          onClick={handleStartGame}
          disabled={isLoading || !username || (!selectedAI && (!customAIName || !customAIDescription))}
          className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Starting Game...' : 'Start Game'}
        </button>
      </div>
    </div>
  );
}