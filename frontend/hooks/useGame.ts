// hooks/useGame.ts
'use client';

import { useState, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { createGameSession, createGameRound, submitGameRound, endGameSession } from '../utils/api'
import { useGameStore } from '../store/gameStore'
import { WhiteCard, GameResult } from '../types'

export const useGame = () => {
  const queryClient = useQueryClient()
  const { gameSession, setGameSession, setCurrentRound, setBlackCard, setWhiteCards } = useGameStore()
  const [selectedCards, setSelectedCards] = useState<WhiteCard[]>([])
  const [showJudgeModal, setShowJudgeModal] = useState(false)
  const [showFinalResultsModal, setShowFinalResultsModal] = useState(false)
  const [aiChosenCards, setAiChosenCards] = useState<WhiteCard[]>([])
  const [judgeExplanation, setJudgeExplanation] = useState('')
  const [gameResult, setGameResult] = useState<GameResult | null>(null)

  const createSessionMutation = useMutation({
    mutationFn: createGameSession,
    onSuccess: (data) => {
      setGameSession(data)
      queryClient.invalidateQueries(['gameRound', data.id])
    },
  })

  const { data: roundData, refetch: refetchRound } = useQuery({
    queryKey: ['gameRound', gameSession?.id],
    queryFn: () => gameSession ? createGameRound(gameSession.id) : null,
    enabled: !!gameSession,
    onSuccess: (data) => {
      if (data) {
        setCurrentRound(data.game_round)
        setBlackCard(data.black_card)
        setWhiteCards(data.white_cards)
        setSelectedCards([])
      }
    },
  })

  const submitRoundMutation = useMutation({
    mutationFn: submitGameRound,
    onSuccess: (data) => {
      setAiChosenCards(data.ai_chosen_cards)
      setJudgeExplanation(data.game_round.judge_explanation)
      setShowJudgeModal(true)
      queryClient.invalidateQueries(['gameRound', gameSession?.id])
    },
  })

  const endGameMutation = useMutation({
    mutationFn: () => gameSession ? endGameSession(gameSession.id) : Promise.reject('No game session'),
    onSuccess: (data) => {
      setGameResult({
        playerScore: data.user_score,
        aiScore: data.ai_score,
        winner: data.winner as 'human' | 'ai' | 'tie',
      })
      setShowFinalResultsModal(true)
    },
  })

  const handleCardSelect = useCallback((card: WhiteCard) => {
    setSelectedCards((prev) => {
      if (prev.find((c) => c.id === card.id)) {
        return prev.filter((c) => c.id !== card.id)
      } else if (prev.length < (roundData?.black_card.pick || 1)) {
        return [...prev, card]
      }
      return prev
    })
  }, [roundData?.black_card.pick])

  const handleSubmitCards = useCallback(() => {
    if (roundData?.game_round && selectedCards.length === roundData.black_card.pick) {
      submitRoundMutation.mutate({
        roundId: roundData.game_round.id,
        userCardIds: selectedCards.map((c) => c.id),
        whiteCardIds: roundData.white_cards.map((c) => c.id),
      })
    }
  }, [roundData, selectedCards, submitRoundMutation])

  const handleNextRound = useCallback(() => {
    setShowJudgeModal(false)
    refetchRound()
  }, [refetchRound])

  const handlePlayAgain = useCallback(() => {
    setShowFinalResultsModal(false)
    refetchRound()
  }, [refetchRound])

  const startGame = useCallback((username: string, aiPersonalityId: number) => {
    createSessionMutation.mutate({ username, ai_personality_id: aiPersonalityId })
  }, [createSessionMutation])

  const endGame = useCallback(() => {
    endGameMutation.mutate()
  }, [endGameMutation])

  return {
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
    startGame,
    endGame,
    setShowFinalResultsModal,
    setGameSession,
  }
}