'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Bell, Menu, X, Zap, Globe2, TrendingUp, Newspaper } from 'lucide-react';
import Link from 'next/link';

const NAV_LINKS = [
  { label: 'Home', href: '/', icon: Newspaper },
  { label: 'Trending', href: '/#trending', icon: TrendingUp },
  { label: 'Navigator', href: '/#features', icon: Globe2 },
  { label: 'Story Arcs', href: '/#concierge', icon: Zap },
];

interface NavbarProps {
  onSignIn?: () => void;
  onSearch?: (query: string) => void;
}

export default function Navbar({ onSignIn, onSearch }: NavbarProps) {
  const [scrolled, setScrolled] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchFocused, setSearchFocused] = useState(false);

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handler, { passive: true });
    return () => window.removeEventListener('scroll', handler);
  }, []);

  const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && searchQuery.trim()) {
      onSearch?.(searchQuery);
      setSearchFocused(false);
    }
  };

  return (
    <motion.nav
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      transition={{ type: 'spring', stiffness: 100, damping: 20 }}
      className="glass-nav"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 50,
        transition: 'box-shadow 0.3s ease',
        boxShadow: scrolled ? '0 8px 32px rgba(0,0,0,0.06)' : 'none',
      }}
    >
      <div className="container" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: 64,
      }}>
        {/* Logo */}
        <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 36,
            height: 36,
            borderRadius: 10,
            background: 'var(--gradient-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 800,
            fontSize: 16,
            color: '#ffffff',
          }}>
            AI
          </div>
          <span style={{ fontWeight: 700, fontSize: 18, letterSpacing: '-0.5px' }}>
            News<span className="text-gradient" style={{ marginLeft: 2 }}>AI</span>
          </span>
        </Link>

        {/* Desktop Nav */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 4,
        }}>
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                padding: '8px 16px',
                borderRadius: 'var(--radius-full)',
                fontSize: 14,
                fontWeight: 500,
                color: 'var(--text-secondary)',
                transition: 'all 0.2s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(220,38,38,0.05)';
                e.currentTarget.style.color = 'var(--accent-crimson)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
                e.currentTarget.style.color = 'var(--text-secondary)';
              }}
            >
              <link.icon size={16} />
              <span className="nav-label">{link.label}</span>
            </Link>
          ))}
        </div>

        {/* Right Side */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div className="glass-input" style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '8px 14px',
            width: 220,
            position: 'relative',
          }}>
            <Search size={14} style={{ color: 'var(--text-tertiary)' }} />
            <input
              type="text"
              placeholder="Search news..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onFocus={() => setSearchFocused(true)}
              onBlur={() => setTimeout(() => setSearchFocused(false), 200)}
              onKeyDown={handleSearch}
              style={{
                background: 'transparent',
                border: 'none',
                outline: 'none',
                color: 'var(--text-primary)',
                fontSize: 13,
                width: '100%',
              }}
            />
          </div>

          <button style={{
            position: 'relative',
            padding: 8,
            borderRadius: 'var(--radius-md)',
            transition: 'all 0.2s',
          }}>
            <Bell size={18} style={{ color: 'var(--text-secondary)' }} />
            <span style={{
              position: 'absolute',
              top: 6,
              right: 6,
              width: 6,
              height: 6,
              borderRadius: '50%',
              background: 'var(--accent-red)',
            }} />
          </button>

          <button
            className="btn-primary"
            style={{ padding: '8px 18px', fontSize: 13 }}
            onClick={() => onSignIn?.()}
          >
            Sign In
          </button>
        </div>
      </div>

      {/* Mobile nav styles are handled via responsive media queries */}
      <style jsx>{`
        @media (max-width: 768px) {
          .nav-label { display: none; }
        }
      `}</style>
    </motion.nav>
  );
}
