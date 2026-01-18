import React, { useState, useRef, useEffect } from 'react';
import { chatWithBot } from './api';
import ReactMarkdown from 'react-markdown';
import { Send, Trash2, Sparkles, BookOpen, Brain, Clock, Bot } from 'lucide-react';

// Assets (Assuming they are placed in src/assets)
import logoImg from './assets/logo.png';
import botAvatar from './assets/bot.png';
import userAvatar from './assets/user.png';

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: "Hi! I'm **StudyBot**.  \nWhat would you like to learn about today?"
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  // introActive and warping states removed

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // constant session ID for this browser refresh instance
  const [sessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);

  const inputRef = useRef(null);

  useEffect(() => {
    // Focus input on load
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (!loading) {
      inputRef.current?.focus();
    }
  }, [loading]);

  const handleSend = async (msg = input) => {
    if (!msg.trim()) return;

    const userMessage = { role: 'user', content: msg };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    // Keep focus
    setTimeout(() => inputRef.current?.focus(), 10);

    try {
      // Pass the unique sessionId to the backend
      const botReplyText = await chatWithBot(msg, sessionId);
      const botMessage = { role: 'bot', content: botReplyText };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: "Sorry, I'm having trouble connecting right now." }]);
    } finally {
      setLoading(false);
      // Ensure focus returns after loading
      setTimeout(() => inputRef.current?.focus(), 10);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  const clearChat = () => {
    setMessages([
      {
        role: 'bot',
        content: "Hi! I'm **StudyBot**.  \nWhat would you like to learn about today?"
      }
    ]);
  };

  const suggestedTopics = [
    { icon: <BookOpen size={18} />, text: "Create a study plan for Biology" },
    { icon: <Brain size={18} />, text: "Quiz me on World History" },
    { icon: <Sparkles size={18} />, text: "Explain Quantum Physics simply" },
    { icon: <Clock size={18} />, text: "Tips for managing exam stress" },
  ];

  return (
    <div className="flex flex-col h-screen app-bg text-slate-100 font-sans relative selection:bg-blue-500/30">

      {/* --- BACKGROUND: HORIZON GLOW --- */}
      <div className="horizon-chat-background animate-fade-in-slow">
        <div className="horizon-glow"></div>
        <div className="horizon-atmosphere"></div>
      </div>

      {/* --- BACKGROUND: HORIZON GLOW --- */}
      <div className="horizon-chat-background animate-fade-in-slow">
        <div className="horizon-glow"></div>
        <div className="horizon-atmosphere"></div>
      </div>

      {/* Header */}
      <header className="relative z-10 pt-8 pb-4 px-6 md:px-12 flex items-start justify-between">
        <div className="w-24 hidden md:block"></div>

        <div className="flex flex-col items-center flex-1">
          <div className="flex items-center gap-3 mb-1">
            <div className="relative">
              <div className="absolute inset-0 bg-blue-500 blur-lg opacity-50 rounded-full"></div>
              <img src={botAvatar} alt="StudyBot" className="relative w-12 h-12 rounded-xl shadow-lg border border-white/10 object-cover bg-slate-900" />
            </div>
            <h1 className="text-3xl font-bold text-white tracking-wide drop-shadow-[0_2px_10px_rgba(59,130,246,0.5)]">StudyBot</h1>
          </div>
          <div className="flex items-center gap-2 mt-1.5 animate-fade-in-slow bg-blue-500/10 px-3 py-1 rounded-full border border-blue-500/20">
            <Bot className="w-3.5 h-3.5 text-blue-300" />
            <span className="text-xs font-medium text-blue-100 tracking-wide uppercase">Your Smart Study Buddy</span>
          </div>
        </div>

        <div className="w-24 hidden md:block"></div>
      </header>

      {/* Chat Area */}
      <main className="relative z-10 flex-1 overflow-y-auto px-4 md:px-20 lg:px-60 py-6 space-y-5 scroll-smooth custom-scrollbar">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'bot' && (
              <div className="relative group mt-1">
                <div className="absolute inset-0 bg-blue-500/30 blur-md rounded-full opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <img
                  src={botAvatar}
                  alt="Bot"
                  className="relative w-8 h-8 rounded-full shadow-lg border border-white/10 object-cover bg-slate-900"
                />
              </div>
            )}

            <div
              className={`relative max-w-[85%] md:max-w-[75%] px-4 py-3 shadow-xl backdrop-blur-xl animate-fade-slide-up ${msg.role === 'user'
                ? 'bubble-user text-white rounded-[20px] rounded-tr-sm'
                : 'bubble-bot text-blue-50 rounded-[20px] rounded-tl-sm'
                }`}
            >
              <div className="prose prose-invert prose-p:leading-snug prose-p:my-0 prose-headings:text-inherit prose-strong:text-blue-300 text-[15px]">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              </div>
            </div>

            {msg.role === 'user' && (
              <img
                src={userAvatar}
                alt="User"
                className="w-8 h-8 rounded-full shadow-lg border border-white/10 object-cover bg-indigo-900 mt-1"
              />
            )}
          </div>
        ))}

        {messages.length === 1 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto mt-12 animate-fade-slide-up" style={{ animationDelay: '0.2s' }}>
            {suggestedTopics.map((topic, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(topic.text)}
                className="flex items-center gap-3 p-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl transition-all hover:scale-105 hover:shadow-lg hover:shadow-blue-500/10 text-left group"
              >
                <div className="p-2 bg-blue-500/20 rounded-lg text-blue-300 group-hover:text-blue-200 transition-colors">
                  {topic.icon}
                </div>
                <span className="text-blue-100/90 text-sm font-medium">{topic.text}</span>
              </button>
            ))}
          </div>
        )}

        {loading && (
          <div className="flex items-end gap-4 justify-start">
            <div className="w-10 h-10 flex items-center justify-center">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
            </div>
            <div className="bubble-bot px-6 py-5 rounded-[24px] rounded-bl-[4px]">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-blue-400/80 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-blue-400/80 rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-blue-400/80 rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} className="h-6" />
      </main>

      {/* Floating Input Area */}
      <footer className="relative z-20 p-6 pb-8">
        <div className="max-w-4xl mx-auto glass-input rounded-full flex items-center p-1.5 shadow-2xl shadow-indigo-900/20 ring-1 ring-white/10">
          <input
            ref={inputRef}
            type="text"
            className="flex-1 bg-transparent border-none text-white px-6 py-3 placeholder-blue-200/30 focus:outline-none focus:ring-0 text-lg font-light tracking-wide"
            placeholder="Ask anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
          />

          <div className="flex items-center gap-1 pr-1.5">
            <button
              onClick={() => handleSend()}
              disabled={loading || !input.trim()}
              className="p-3.5 bg-gradient-to-br from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 rounded-full transition-all disabled:opacity-50 disabled:scale-95 shadow-lg shadow-blue-500/30 group hover:scale-[1.05]"
            >
              <Send className="w-5 h-5 text-white group-hover:translate-x-0.5 transition-transform" strokeWidth={2} />
            </button>
            <div className="w-px h-6 bg-white/10 mx-2"></div>
            <button
              onClick={clearChat}
              className="p-3.5 hover:bg-white/10 rounded-full transition-all text-blue-200/50 hover:text-red-300 group"
              title="Clear Chat"
            >
              <Trash2 className="w-5 h-5 group-hover:rotate-12 transition-transform" strokeWidth={1.5} />
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
