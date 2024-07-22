import React, { useState } from 'react';
import HomePage from './components/HomePage';
import GamePage from './components/GamePage';

export default function App() {
  const [gameData, setGameData] = useState(null);

  const handleGameStart = (initialGameData) => {
    console.log('Game started with data:', initialGameData);
    setGameData(initialGameData);
  };

  const handleReturnHome = () => {
    setGameData(null);
  };

  return (
    <div className="App">
      {gameData ? (
        <GamePage initialGameData={gameData} onReturnHome={handleReturnHome} />
      ) : (
        <HomePage onGameStart={handleGameStart} />
      )}
    </div>
  );
}