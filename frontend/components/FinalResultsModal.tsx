// components/FinalResultsModal.tsx
import React from 'react'

interface FinalResultsModalProps {
  playerScore: number
  aiScore: number
  winner: 'human' | 'ai' | 'tie'
  onPlayAgain: () => void
  onChangeAI: () => void
}

const FinalResultsModal: React.FC<FinalResultsModalProps> = ({
  playerScore,
  aiScore,
  winner,
  onPlayAgain,
  onChangeAI,
}) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">Game Over</h2>
        <div className="mb-4">
          <h3 className="text-xl font-semibold mb-2">Final Scores:</h3>
          <p className="text-lg">You: {playerScore}</p>
          <p className="text-lg">AI: {aiScore}</p>
        </div>
        <div className="mb-4">
          <h3 className="text-xl font-semibold mb-2">Winner:</h3>
          <p className={`text-2xl font-bold ${winner === 'human' ? 'text-blue-600' : winner === 'ai' ? 'text-green-600' : 'text-gray-600'}`}>
            {winner === 'human' ? 'You Win!' : winner === 'ai' ? 'AI Wins!' : 'It\'s a Tie!'}
          </p>
        </div>
        <div className="flex justify-between">
          <button
            onClick={onPlayAgain}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Play Again
          </button>
          <button
            onClick={onChangeAI}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Change AI Opponent
          </button>
        </div>
      </div>
    </div>
  )
}

export default FinalResultsModal