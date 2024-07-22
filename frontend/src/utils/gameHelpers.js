export const calculateWinner = (userScore, aiScore) => {
    if (userScore > aiScore) return 'User';
    if (aiScore > userScore) return 'AI';
    return 'Tie';
  };
  
  export const formatRoundNumber = (roundNumber) => {
    return `Round ${roundNumber}`;
  };