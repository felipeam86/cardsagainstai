// utils/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
})

export const getAIPersonalities = async () => {
  console.log('Fetching AI personalities...')
  try {
    const response = await api.get('/ai-personalities')
    console.log('AI personalities fetched:', response.data)
    return response.data
  } catch (error) {
    console.error('Error fetching AI personalities:', error)
    throw error
  }
}

export const createGameSession = async ({ username, ai_personality_id }: { username: string; ai_personality_id: number }) => {
  console.log('Creating game session...', { username, ai_personality_id })
  try {
    const response = await api.post('/game-sessions', { username, ai_personality_id })
    console.log('Game session created:', response.data)
    return response.data
  } catch (error) {
    console.error('Error creating game session:', error)
    throw error
  }
}

export const createGameRound = async (gameSessionId: number) => {
  console.log('Creating game round...', { gameSessionId })
  try {
    const response = await api.post('/game-rounds', { game_session_id: gameSessionId })
    console.log('Game round created:', response.data)
    return response.data
  } catch (error) {
    console.error('Error creating game round:', error)
    throw error
  }
}

export const submitGameRound = async ({ roundId, userCardIds, whiteCardIds }: { roundId: number; userCardIds: number[]; whiteCardIds: number[] }) => {
  console.log('Submitting game round...', { roundId, userCardIds, whiteCardIds })
  try {
    const response = await api.post(`/game-rounds/${roundId}/submit`, { user_card_ids: userCardIds, white_card_ids: whiteCardIds })
    console.log('Game round submitted:', response.data)
    return response.data
  } catch (error) {
    console.error('Error submitting game round:', error)
    throw error
  }
}

export const endGameSession = async (sessionId: number) => {
  console.log('Ending game session...', { sessionId })
  try {
    const response = await api.post(`/game-sessions/${sessionId}/end`)
    console.log('Game session ended:', response.data)
    return response.data
  } catch (error) {
    console.error('Error ending game session:', error)
    throw error
  }
}