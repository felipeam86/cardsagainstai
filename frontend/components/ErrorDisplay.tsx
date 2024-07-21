// components/ErrorDisplay.tsx
import React from 'react'

interface ErrorDisplayProps {
  error: Error;
}

const ErrorDisplay: React.FC<ErrorDisplayProps> = ({ error }) => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-red-100 text-red-800 p-4">
      <h1 className="text-2xl font-bold mb-4">An error occurred</h1>
      <p className="mb-2">{error.message}</p>
      <p className="text-sm">Please check the console for more details.</p>
    </div>
  )
}

export default ErrorDisplay