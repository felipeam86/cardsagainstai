// store/gameStore.ts
import create from 'zustand'
import { AIPersonality, GameSession, GameRound, BlackCard, WhiteCard } from '../types'

interface GameStore {
  aiPersonalities: AIPersonality[]
  setAIPersonalities: (personalities: AIPersonality[]) => void
  gameSession: GameSession | null
  setGameSession: (session: GameSession | null) => void
  currentRound: GameRound | null
  setCurrentRound: (round: GameRound | null) => void
  blackCard: BlackCard | null
  setBlackCard: (card: BlackCard | null) => void
  whiteCards: WhiteCard[]
  setWhiteCards: (cards: WhiteCard[]) => void
  selectedCards: WhiteCard[]
  setSelectedCards: (cards: WhiteCard[]) => void
}

export const useGameStore = create<GameStore>((set) => ({
  aiPersonalities: [],
  setAIPersonalities: (personalities) => set({ aiPersonalities: personalities }),
  gameSession: null,
  setGameSession: (session) => set({ gameSession: session }),
  currentRound: null,
  setCurrentRound: (round) => set({ currentRound: round }),
  blackCard: null,
  setBlackCard: (card) => set({ blackCard: card }),
  whiteCards: [],
  setWhiteCards: (cards) => set({ whiteCards: cards }),
  selectedCards: [],
  setSelectedCards: (cards) => set({ selectedCards: cards }),
}))