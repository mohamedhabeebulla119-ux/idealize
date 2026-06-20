import React, { useState } from 'react';
import { sendQuery } from '../services/api';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    try {
      const response = await sendQuery(input);
      setMessages(prev => [...prev, { sender: 'ai', text: response.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'ai', text: 'Error connecting to backend.' }]);
    }
  };

  return (
    <div className="chat-interface">
      <div className="messages-window" style={{ minHeight: '200px', border: '1px solid #444', padding: '10px' }}>
        {messages.map((m, idx) => (
          <div key={idx} className={`msg ${m.sender}`}>
            <strong>{m.sender === 'user' ? 'You: ' : 'TradePilot: '}</strong>{m.text}
          </div>
        ))}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} placeholder="Ask about HS codes, customs duties..." />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default ChatInterface;
