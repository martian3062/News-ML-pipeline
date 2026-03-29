'use client';

import { motion } from 'framer-motion';
import { X, Play } from 'lucide-react';

export default function DemoModal({ onClose }: { onClose: () => void }) {
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
        style={{ maxWidth: 560, textAlign: 'center' }}
      >
        <button className="modal-close" onClick={onClose}>
          <X size={16} />
        </button>

        {/* Demo video placeholder */}
        <div style={{
          borderRadius: 'var(--radius-md)',
          overflow: 'hidden',
          background: 'linear-gradient(135deg, rgba(220,38,38,0.08), rgba(225,29,72,0.06))',
          height: 260,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: 24,
          position: 'relative',
        }}>
          <div style={{
            position: 'absolute', inset: 0,
            background: 'radial-gradient(ellipse, rgba(220,38,38,0.1) 0%, transparent 70%)',
          }} />
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            style={{
              width: 72, height: 72, borderRadius: '50%',
              background: 'var(--gradient-primary)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 0 40px rgba(220,38,38,0.3)',
              cursor: 'pointer',
            }}
          >
            <Play size={28} style={{ color: '#fff', marginLeft: 3 }} />
          </motion.div>
        </div>

        <h2 style={{ fontSize: 22, fontWeight: 800, marginBottom: 8 }}>
          Platform <span className="text-gradient">Walkthrough</span>
        </h2>
        <p style={{ fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: 24 }}>
          Watch how NewsAI uses Gemini & Groq to synthesize hundreds of news sources
          into personalized, actionable intelligence — in under 60 seconds.
        </p>

        <div style={{
          display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12,
          padding: 16, borderRadius: 'var(--radius-md)',
          background: 'rgba(0,0,0,0.02)',
        }}>
          {[
            { label: 'AI Briefings', time: '0:00' },
            { label: 'Story Arcs', time: '0:22' },
            { label: 'Concierge', time: '0:41' },
          ].map((ch) => (
            <div key={ch.label} style={{
              padding: '8px 0', cursor: 'pointer',
              borderRadius: 'var(--radius-sm)',
              transition: 'background 0.2s',
            }}>
              <p style={{ fontSize: 12, fontWeight: 600 }}>{ch.label}</p>
              <p style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>{ch.time}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
}
