// components/WhiteCard.tsx
import React from 'react'
import { WhiteCard as WhiteCardType } from '../types'

interface WhiteCardProps {
  card: WhiteCardType
  isSelected: boolean
  onSelect: (card: WhiteCardType) => void
}

const WhiteCard: React.FC<WhiteCardProps> = ({ card, isSelected, onSelect }) => {
  return (
    <div
      className={`bg-white p-4 rounded-lg shadow-md cursor-pointer transition-all duration-200 ${
        isSelected ? 'ring-4 ring-blue-500' : 'hover:shadow-lg'
      }`}
      onClick={() => onSelect(card)}
    >
      <p className="text-lg mb-2">{card.text}</p>
      <p className="text-right text-xs text-gray-400">{card.watermark}</p>
    </div>
  )
}

export default WhiteCard