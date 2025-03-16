import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSendMessage = async () => {
    if (input.trim() === '') return;
  
    const newMessage = { text: input, sender: 'You' };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
  
    try {
      const response = await fetch(`https://n8n.my-assistant.co.za/webhook/search?q=${encodeURIComponent(input)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
  
      console.log("Agent Response:", response);
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("Parsed Response:", data);
  
      if (data && data.output) {
        setMessages((prevMessages) => [...prevMessages, { text: data.output, sender: 'Bot' }]);
      } else {
        setMessages((prevMessages) => [...prevMessages, { text: "No valid response from the bot.", sender: 'Bot' }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [...prevMessages, { text: 'Error retrieving response.', sender: 'Bot' }]);
    }
  
    setInput('');
  };

  return (
    <div className="chat-app">
      <header className="chat-header">
        <h1>My assistant</h1>
      </header>
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender === 'You' ? 'user' : 'bot'}`}>
              <span className="sender">{msg.sender}</span>
              <p className="text">{msg.text}</p>
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="chat-input"
          />
          <button onClick={handleSendMessage} className="send-button">Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;