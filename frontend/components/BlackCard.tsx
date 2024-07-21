// components/BlackCard.tsx
import React from 'react'
import { BlackCard as BlackCardType } from '../types'

interface BlackCardProps {
  card: BlackCardType
}

const BlackCard: React.FC<BlackCardProps> = ({ card }) => {
  return (
    <div className="bg-gray-800 text-white p-6 rounded-lg shadow-lg max-w-sm">
      <p className="text-xl mb-4">{card.text}</p>
      <div className="flex justify-between items-center text-sm">
        <span>Pick: {card.pick}</span>
        <span className="text-gray-400">{card.watermark}</span>
      </div>
    </div>
  )
}

export default BlackCard