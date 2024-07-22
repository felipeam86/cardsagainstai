import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/';

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchAIPersonalities = () => apiClient.get('/ai-personalities');

export const createAIPersonality = (name, description) => 
  apiClient.post('/ai-personalities', { name, description });

export const createGameSession = (username, aiPersonalityId) => 
  apiClient.post('/game-sessions', { username, ai_personality_id: aiPersonalityId });

export const createGameRound = (gameSessionId) => 
  apiClient.post('/game-rounds', { game_session_id: gameSessionId });

export const submitGameRound = (roundId, userCardIds, whiteCardIds) => 
  apiClient.post(`/game-rounds/${roundId}/submit`, { user_card_ids: userCardIds, white_card_ids: whiteCardIds });

export const endGameSession = (sessionId) => 
  apiClient.post(`/game-sessions/${sessionId}/end`);

export default apiClient;