// components/JudgeDecisionModal.tsx
import React from 'react'
import { BlackCard, WhiteCard } from '../types'

interface JudgeDecisionModalProps {
  blackCard: BlackCard
  playerCards: WhiteCard[]
  aiCards: WhiteCard[]
  winner: 'human' | 'ai' | 'tie'
  explanation: string
  onClose: () => void
}

const JudgeDecisionModal: React.FC<JudgeDecisionModalProps> = ({
  blackCard,
  playerCards,
  aiCards,
  winner,
  explanation,
  onClose,
}) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg max-w-2xl w-full">
        <h2 className="text-2xl font-bold mb-4">Judge's Decision</h2>
        <div className="mb-4">
          <h3 className="text-xl font-semibold mb-2">Black Card:</h3>
          <p className="bg-gray-800 text-white p-4 rounded">{blackCard.text}</p>
        </div>
        <div className="flex mb-4">
          <div className="w-1/2 pr-2">
            <h3 className="text-xl font-semibold mb-2">Your Cards:</h3>
            {playerCards.map((card) => (
              <p key={card.id} className="bg-blue-100 p-2 rounded mb-2">
                {card.text}
              </p>
            ))}
          </div>
          <div className="w-1/2 pl-2">
            <h3 className="text-xl font-semibold mb-2">AI's Cards:</h3>
            {aiCards.map((card) => (
              <p key={card.id} className="bg-green-100 p-2 rounded mb-2">
                {card.text}
              </p>
            ))}
          </div>
        </div>
        <div className="mb-4">
          <h3 className="text-xl font-semibold mb-2">Winner:</h3>
          <p className={`text-lg font-bold ${winner === 'human' ? 'text-blue-600' : winner === 'ai' ? 'text-green-600' : 'text-gray-600'}`}>
            {winner === 'human' ? 'You' : winner === 'ai' ? 'AI' : 'Tie'}
          </p>
        </div>
        <div className="mb-4">
          <h3 className="text-xl font-semibold mb-2">Explanation:</h3>
          <p>{explanation}</p>
        </div>
        <button
          onClick={onClose}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Next Round
        </button>
      </div>
    </div>
  )
}

export default JudgeDecisionModal