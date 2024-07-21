// components/GamePage.tsx
'use client';

import React from 'react'
import { useRouter } from 'next/navigation'
import { useGame } from '../hooks/useGame'
import BlackCard from './BlackCard'
import WhiteCard from './WhiteCard'
import ScoreBoard from './ScoreBoard'
import JudgeDecisionModal from './JudgeDecisionModal'
import FinalResultsModal from './FinalResultsModal'

const GamePage: React.FC = () => {
  const router = useRouter()
  const {
    gameSession,
    roundData,
    selectedCards,
    showJudgeModal,
    showFinalResultsModal,
    aiChosenCards,
    judgeExplanation,
    gameResult,
    handleCardSelect,
    handleSubmitCards,
    handleNextRound,
    handlePlayAgain,
    endGame,
    setShowFinalResultsModal,
    setGameSession
  } = useGame()

  const handleChangeAI = () => {
    setShowFinalResultsModal(false)
    setGameSession(null)
    router.push('/')
  }


  if (!gameSession || !roundData) return null

  const { game_round: currentRound, black_card: blackCard, white_cards: whiteCards } = roundData

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <header className="bg-gray-800 text-white p-4">
        <h1 className="text-2xl font-bold">Cards Against AI</h1>
      </header>
      <main className="flex-1 flex p-4">
        <div className="w-1/3 pr-4">
          <div className="bg-gray-900 p-4 rounded-lg shadow-lg mb-4">
            <BlackCard card={blackCard} />
          </div>
          <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
            <ScoreBoard
              playerScore={currentRound.user_score}
              aiScore={currentRound.ai_score}
              currentRound={currentRound.round_number}
            />
          </div>
        </div>
        <div className="w-2/3 bg-white p-4 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-4">Your Hand</h2>
          <div className="grid grid-cols-3 gap-4">
            {whiteCards.map((card) => (
              <WhiteCard
                key={card.id}
                card={card}
                isSelected={selectedCards.some((c) => c.id === card.id)}
                onSelect={handleCardSelect}
              />
            ))}
          </div>
        </div>
      </main>
      <footer className="bg-gray-200 p-4">
        <div className="flex justify-between items-center max-w-6xl mx-auto">
          <div>
            <span className="mr-2">Selected cards: {selectedCards.length}</span>
            <span>/ {blackCard.pick}</span>
          </div>
          <div>
            <button
              onClick={handleSubmitCards}
              disabled={selectedCards.length !== blackCard.pick}
              className="bg-blue-500 text-white px-4 py-2 rounded mr-2 disabled:bg-gray-400 hover:bg-blue-600 transition-colors"
            >
              Submit Cards
            </button>
            <button
              onClick={endGame}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors"
            >
              End Game
            </button>
          </div>
        </div>
      </footer>
      {showJudgeModal && (
        <JudgeDecisionModal
          blackCard={blackCard}
          playerCards={selectedCards}
          aiCards={aiChosenCards}
          winner={currentRound.winner as 'human' | 'ai' | 'tie'}
          explanation={judgeExplanation}
          onClose={handleNextRound}
        />
      )}
      {showFinalResultsModal && gameResult && (
        <FinalResultsModal
          playerScore={gameResult.playerScore}
          aiScore={gameResult.aiScore}
          winner={gameResult.winner}
          onPlayAgain={handlePlayAgain}
          onChangeAI={handleChangeAI}
        />
      )}
    </div>
  )
}

export default GamePage