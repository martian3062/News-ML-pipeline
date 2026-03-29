'use client';

import { motion } from 'framer-motion';
import { X } from 'lucide-react';

export default function SignInModal({ onClose }: { onClose: () => void }) {
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
      >
        <button className="modal-close" onClick={onClose}>
          <X size={16} />
        </button>

        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <div style={{
            width: 56, height: 56, borderRadius: 16,
            background: 'var(--gradient-primary)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 16px',
            fontSize: 22, fontWeight: 800, color: '#fff',
          }}>AI</div>
          <h2 style={{ fontSize: 22, fontWeight: 800, marginBottom: 6 }}>
            Welcome to <span className="text-gradient">NewsAI</span>
          </h2>
          <p style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
            Sign in to personalize your news experience
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          <input
            className="glass-input"
            type="email"
            placeholder="Email address"
            style={{ width: '100%' }}
          />
          <input
            className="glass-input"
            type="password"
            placeholder="Password"
            style={{ width: '100%' }}
          />
          <button className="btn-primary" style={{
            width: '100%', justifyContent: 'center', padding: '14px 24px', fontSize: 15, marginTop: 4,
          }}>
            Sign In
          </button>
        </div>

        <p style={{
          textAlign: 'center', marginTop: 20,
          fontSize: 13, color: 'var(--text-tertiary)',
        }}>
          Don&apos;t have an account?{' '}
          <span style={{ color: 'var(--accent-crimson)', fontWeight: 600, cursor: 'pointer' }}>
            Create one for free
          </span>
        </p>
      </motion.div>
    </motion.div>
  );
}
