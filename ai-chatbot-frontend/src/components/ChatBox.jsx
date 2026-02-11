// ChatBox.jsx
import { useState, useEffect, useRef, useCallback } from "react";
import "../styles/ChatBox.css";

const API_URL = process.env.REACT_APP_API_URL;

function ChatBox({ user, onLogout }) {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [chatHistory, setChatHistory] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [theme, setTheme] = useState('dark');
  const chatBoxRef = useRef(null);

  // Load chat history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('chatHistory');
    if (savedHistory) {
      setChatHistory(JSON.parse(savedHistory));
    }
  }, []);

  // Auto scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chat, loading]);

  const saveCurrentChatToHistory = useCallback((title, currentChat, currentHistory) => {
    const newChat = {
      id: Date.now(),
      title: title.substring(0, 30) + (title.length > 30 ? '...' : ''),
      messages: currentChat,
      timestamp: new Date().toISOString()
    };

    const updatedHistory = [newChat, ...currentHistory];
    setChatHistory(updatedHistory);
    localStorage.setItem('chatHistory', JSON.stringify(updatedHistory));
    setActiveChatId(newChat.id);
  }, []);

  // Save current chat to history when it has messages
  useEffect(() => {
    if (chat.length > 0 && !activeChatId) {
      const firstUserMessage = chat.find(msg => msg.sender === 'user');
      if (firstUserMessage && chatHistory.length === 0) {
        saveCurrentChatToHistory(firstUserMessage.text, chat, chatHistory);
      }
    }
  }, [chat, activeChatId, chatHistory, saveCurrentChatToHistory]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;
    const newUserMsg = { sender: "user", text: userMessage };
    
    setChat(prev => [...prev, newUserMsg]);
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });
      if (!response.ok) {
        throw new Error("Server error");
      }
      const data = await response.json();
      
      const botMessage = { sender: "bot", text: data.reply };
      setChat(prev => {
        const updatedChat = [...prev, botMessage];
        
        // Update chat history if this is an existing chat
        if (activeChatId) {
          updateChatHistory(activeChatId, updatedChat);
        }
        
        return updatedChat;
      });
    } catch (error) {
      const errorMsg = { sender: "bot", text: "⚠️ Server error. Try again." };
      setChat(prev => {
        const updatedChat = [...prev, errorMsg];
        
        if (activeChatId) {
          updateChatHistory(activeChatId, updatedChat);
        }
        
        return updatedChat;
      });
    } finally {
      setLoading(false);
    }
  };

  const updateChatHistory = (chatId, updatedMessages) => {
    setChatHistory(prev => {
      const updatedHistory = prev.map(c => 
        c.id === chatId ? { ...c, messages: updatedMessages } : c
      );
      localStorage.setItem('chatHistory', JSON.stringify(updatedHistory));
      return updatedHistory;
    });
  };

  const startNewChat = () => {
    // Save current chat if it has messages and isn't already saved
    if (chat.length > 0 && !activeChatId) {
      const firstUserMessage = chat.find(msg => msg.sender === 'user');
      if (firstUserMessage) {
        saveCurrentChatToHistory(firstUserMessage.text, chat, chatHistory);
      }
    }
    
    setChat([]);
    setActiveChatId(null);
    setMessage("");
  };

  const loadChatHistory = (chatId) => {
    const selectedChat = chatHistory.find(c => c.id === chatId);
    if (selectedChat) {
      setChat(selectedChat.messages);
      setActiveChatId(chatId);
    }
  };

  const deleteChatHistory = (chatId, e) => {
    e.stopPropagation();
    const updatedHistory = chatHistory.filter(c => c.id !== chatId);
    setChatHistory(updatedHistory);
    localStorage.setItem('chatHistory', JSON.stringify(updatedHistory));
    
    if (activeChatId === chatId) {
      setChat([]);
      setActiveChatId(null);
    }
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('chatHistory');
    onLogout();
  };

  return (
    <div className={`chat-container ${theme}`}>
      {/* Sidebar */}
      <div className={`sidebar ${!sidebarOpen ? 'closed' : ''}`}>
        <div className="sidebar-header">
          <button className="new-chat-btn" onClick={startNewChat}>
            New Chat
          </button>
        </div>

        <div className="chat-history">
          {chatHistory.length === 0 ? (
            <div className="no-history">No chat history yet</div>
          ) : (
            chatHistory.map((chatItem) => (
              <div
                key={chatItem.id}
                className={`chat-history-item ${activeChatId === chatItem.id ? 'active' : ''}`}
                onClick={() => loadChatHistory(chatItem.id)}
              >
                <span className="history-title">{chatItem.title}</span>
                <button 
                  className="delete-chat-btn"
                  onClick={(e) => deleteChatHistory(chatItem.id, e)}
                >
                  🗑️
                </button>
              </div>
            ))
          )}
        </div>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-details">
              <div className="user-avatar">
                {user.name.charAt(0).toUpperCase()}
              </div>
              <div className="user-text">
                <div className="user-name">{user.name}</div>
                <div className="user-email">{user.email}</div>
              </div>
            </div>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="main-chat">
        <div className="chat-header">
          <button className="toggle-sidebar-btn" onClick={toggleSidebar}>
            ☰
          </button>
          <h1 className="chat-title">ChatBot AI</h1>
          <button className="theme-toggle-btn" onClick={toggleTheme}>
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
        </div>

        <div className="chat-box" ref={chatBoxRef}>
          {chat.length === 0 && !loading ? (
            <div className="empty-state">
              <h2>How can I help you today?</h2>
              <p>Start a conversation by typing a message below</p>
              <div className="example-prompts">
                <div className="example-prompt" onClick={() => setMessage("What can you help me with?")}>
                  "What can you help me with?"
                </div>
                <div className="example-prompt" onClick={() => setMessage("Tell me a fun fact")}>
                  "Tell me a fun fact"
                </div>
                <div className="example-prompt" onClick={() => setMessage("Explain quantum computing")}>
                  "Explain quantum computing"
                </div>
              </div>
            </div>
          ) : (
            <>
              {chat.map((msg, index) => (
                <div key={index} className={`message ${msg.sender}`}>
                  <div className="message-avatar">
                    {msg.sender === "user" ? user.name.charAt(0).toUpperCase() : "🤖"}
                  </div>
                  <div className="message-content">{msg.text}</div>
                </div>
              ))}
            </>
          )}

          {loading && (
            <div className="typing-indicator">
              <div className="message-avatar">🤖</div>
              <div className="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>

        <div className="input-area">
          <div className="input-wrapper">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type a message..."
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
            />
            <button 
              className="send-button" 
              onClick={sendMessage}
              disabled={!message.trim() || loading}
            >
              Send ✈️
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatBox;
