// components/ScoreBoard.tsx
import React from 'react'
import dynamic from 'next/dynamic'

const User = dynamic(() => import('lucide-react').then((mod) => mod.User), { ssr: false })
const Bot = dynamic(() => import('lucide-react').then((mod) => mod.Bot), { ssr: false })
const Award = dynamic(() => import('lucide-react').then((mod) => mod.Award), { ssr: false })

interface ScoreBoardProps {
  playerScore: number
  aiScore: number
  currentRound: number
}

const ScoreBoard: React.FC<ScoreBoardProps> = ({ playerScore, aiScore, currentRound }) => {
  return (
    <div className="bg-gray-700 text-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Scoreboard</h2>
      <div className="flex justify-between items-center mb-2">
        <div className="flex items-center">
          <User className="mr-2" />
          <span>Player:</span>
        </div>
        <span>{playerScore}</span>
      </div>
      <div className="flex justify-between items-center mb-2">
        <div className="flex items-center">
          <Bot className="mr-2" />
          <span>AI:</span>
        </div>
        <span>{aiScore}</span>
      </div>
      <div className="flex justify-between items-center">
        <div className="flex items-center">
          <Award className="mr-2" />
          <span>Round:</span>
        </div>
        <span>{currentRound}</span>
      </div>
    </div>
  )
}

export default ScoreBoard