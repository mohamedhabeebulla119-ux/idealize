import React from 'react'
import Chat from './pages/Chat'
import { ChatProvider } from './context/ChatContext'

function App() {
  return (
    <ChatProvider>
      <div className="App">
        <Chat />
      </div>
    </ChatProvider>
  )
}

export default App
