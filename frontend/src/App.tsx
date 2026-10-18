/**
 * Main App component for the AI Sycophancy Lab frontend
 */

import { useState, useEffect } from 'react';
import { apiClient } from './api/client';
import type {
  SessionResponse,
  Message,
  MessageResponse,
} from './types/api';
import './index.css';

function App() {
  const [session, setSession] = useState<SessionResponse | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Create session on mount
  useEffect(() => {
    const initSession = async () => {
      try {
        setError(null);
        const sessionResponse = await apiClient.createSession({
          study_id: 'study4_pilot',
          test_mode: true,
          // For testing, you can specify condition: 'C0', 'C1', 'C2', 'C3', 'C4'
          condition: 'C0',
        });
        setSession(sessionResponse);
      } catch (err) {
        setError('Failed to create session. Please refresh the page.');
        console.error(err);
      }
    };

    initSession();
  }, []);

  // Load messages when session changes
  useEffect(() => {
    if (!session) return;

    const loadMessages = async () => {
      try {
        const sessionState = await apiClient.getSessionState(session.session_id);
        setMessages(sessionState.messages);
      } catch (err) {
        console.error('Failed to load messages:', err);
      }
    };

    loadMessages();
  }, [session]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !session || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response: MessageResponse = await apiClient.sendMessage(
        session.session_id,
        { message: userMessage }
      );

      // Add user message and assistant response to messages
      setMessages((prev) => [
        ...prev,
        {
          role: 'user',
          content: userMessage,
          timestamp: new Date().toISOString(),
          turn: response.turn_number,
        },
        {
          role: 'assistant',
          content: response.assistant_message,
          timestamp: new Date().toISOString(),
          turn: response.turn_number,
          model: 'mock-model-v1',
          latency_ms: response.response_latency_ms,
        },
      ]);
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEndSession = async () => {
    if (!session) return;

    try {
      await apiClient.endSession(session.session_id);
      setSession({ ...session, status: 'ended' });
    } catch (err) {
      setError('Failed to end session.');
      console.error(err);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>AI Sycophancy Lab</h1>
      </header>

      <main className="main">
        {error && <div className="error">{error}</div>}

        {session && (
          <div className="session-info">
            <h2>Session Information</h2>
            <p><strong>Session ID:</strong> {session.session_id.slice(0, 8)}...</p>
            <p><strong>Condition:</strong> {session.condition}</p>
            <p><strong>Status:</strong> {session.status}</p>
            <p><strong>Study:</strong> {session.study_id}</p>
          </div>
        )}

        <div className="chat-container">
          <div className="messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'user' ? 'U' : 'AI'}
                </div>
                <div>
                  <div className="message-content">{msg.content}</div>
                  <div className="message-meta">
                    Turn {msg.turn} • {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="loading">
                <span>AI is thinking</span>
                <span className="loading-dots"></span>
              </div>
            )}
          </div>

          <div className="input-area">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={!session || session.status !== 'active' || isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!session || session.status !== 'active' || isLoading}
            >
              Send
            </button>
          </div>
        </div>

        {session && session.status === 'active' && (
          <div className="controls">
            <button onClick={handleEndSession}>End Session</button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
