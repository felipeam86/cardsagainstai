// components/HomePage.tsx
'use client';

import React, { useState } from 'react'
import ErrorDisplay from './ErrorDisplay'
import { useRouter } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'
import { getAIPersonalities } from '../utils/api'
import { useGame } from '../hooks/useGame'

const HomePage: React.FC = () => {
  const router = useRouter()
  const [username, setUsername] = useState('')
  const [selectedAI, setSelectedAI] = useState<number | null>(null)
  const [customAIName, setCustomAIName] = useState('')
  const [showCustomAI, setShowCustomAI] = useState(false)
  const { startGame } = useGame()

  const { data: aiPersonalities, isLoading, isError, error } = useQuery({
    queryKey: ['aiPersonalities'],
    queryFn: getAIPersonalities
  })

  const handleStartGame = () => {
    if (username && selectedAI) {
      console.log('Starting game with:', { username, selectedAI });
      startGame(username, selectedAI);
      router.push('/game');
    }
  };

  if (isLoading) {
    return <div className="flex justify-center items-center h-screen">Loading AI personalities...</div>
  }

  if (isError) {
    return <ErrorDisplay error={error as Error} />
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">Cards Against AI</h1>
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-2 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select
          value={selectedAI || ''}
          onChange={(e) => setSelectedAI(Number(e.target.value))}
          className="w-full p-2 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select AI Opponent</option>
          {aiPersonalities?.map((ai) => (
            <option key={ai.id} value={ai.id}>
              {ai.name}
            </option>
          ))}
        </select>
        <button
          onClick={() => setShowCustomAI(!showCustomAI)}
          className="w-full p-2 mb-4 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          {showCustomAI ? 'Cancel Custom AI' : 'Add Custom AI'}
        </button>
        {showCustomAI && (
          <input
            type="text"
            placeholder="Enter custom AI name"
            value={customAIName}
            onChange={(e) => setCustomAIName(e.target.value)}
            className="w-full p-2 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )}
        <button
          onClick={handleStartGame}
          disabled={!username || !selectedAI}
          className="w-full p-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Start Game
        </button>
      </div>
    </div>
  )
}

export default HomePage