// app/game/page.tsx
import dynamic from 'next/dynamic'

const GamePage = dynamic(() => import('../../components/GamePage'), { ssr: false })

export default function Game() {
  return <GamePage />
}

