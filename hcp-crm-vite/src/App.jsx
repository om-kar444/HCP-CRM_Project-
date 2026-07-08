import React from 'react'
import FormPanel from './components/FormPanel.jsx'
import ChatPanel from './components/ChatPanel.jsx'

function App() {
  return (
    <div className="App">
      <h1>Log HCP Interaction</h1>
      <div className="layout">
        <FormPanel />
        <ChatPanel />
      </div>
    </div>
  )
}

export default App