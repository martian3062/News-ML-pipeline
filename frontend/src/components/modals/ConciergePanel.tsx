'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { X, Bot } from 'lucide-react';
import { sendConciergeMessage } from '@/lib/api';

export default function ConciergePanel({ onClose }: { onClose: () => void }) {
  const [messages, setMessages] = useState([
    { role: 'bot', text: "Hello! I'm your AI News Concierge. Ask me anything about today's business news, market trends, or get personalized briefings." },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>();

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = input;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', text: userMessage }]);
    setLoading(true);

    try {
      const { response, session_id } = await sendConciergeMessage(userMessage, sessionId);
      if (session_id) setSessionId(session_id);
      
      setMessages((prev) => [...prev, { role: 'bot', text: response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'bot', text: "I'm sorry, I'm having trouble connecting right now. Please try again later." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="modal-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
      style={{ zIndex: 1000 }}
    >
      <motion.div
        className="modal-content"
        initial={{ opacity: 0, y: 40, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 20, scale: 0.98 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: 520, padding: 0, display: 'flex', flexDirection: 'column', maxHeight: '80vh' }}
      >
        {/* Header */}
        <div style={{
          padding: '20px 24px',
          borderBottom: '1px solid rgba(0,0,0,0.06)',
          display: 'flex', alignItems: 'center', gap: 12,
        }}>
          <div style={{
            width: 40, height: 40, borderRadius: 12,
            background: 'var(--gradient-primary)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <Bot size={20} style={{ color: '#fff' }} />
          </div>
          <div style={{ flex: 1 }}>
            <p style={{ fontWeight: 700, fontSize: 15 }}>AI Concierge</p>
            <p style={{ fontSize: 12, color: 'var(--accent-green)' }}>● Online</p>
          </div>
          <button className="modal-close" onClick={onClose} style={{ position: 'static' }}>
            <X size={16} />
          </button>
        </div>

        {/* Messages */}
        <div style={{
          flex: 1, padding: 20, overflowY: 'auto',
          display: 'flex', flexDirection: 'column', gap: 16,
          minHeight: 300,
        }}>
          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '80%',
                padding: '12px 16px',
                borderRadius: msg.role === 'user'
                  ? '16px 16px 4px 16px'
                  : '16px 16px 16px 4px',
                background: msg.role === 'user'
                  ? 'var(--gradient-primary)'
                  : 'rgba(0,0,0,0.04)',
                color: msg.role === 'user' ? '#fff' : 'var(--text-primary)',
                fontSize: 14, lineHeight: 1.6,
              }}
            >
              {msg.text}
            </div>
          ))}
        </div>

        {/* Input */}
        <div style={{
          padding: '16px 20px',
          borderTop: '1px solid rgba(0,0,0,0.06)',
          display: 'flex', gap: 8,
        }}>
          <input
            className="glass-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about today's news..."
            style={{ flex: 1 }}
            disabled={loading}
          />
          <button
            className="btn-primary"
            onClick={handleSend}
            style={{ padding: '10px 18px', opacity: loading ? 0.7 : 1 }}
            disabled={loading}
          >
            {loading ? 'Thinking...' : 'Send'}
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}
