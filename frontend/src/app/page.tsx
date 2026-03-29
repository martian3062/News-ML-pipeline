'use client';

import { useEffect, useState, useRef, useCallback } from 'react';
import dynamic from 'next/dynamic';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowRight, Sparkles, Radio, BarChart3, Globe2,
  Zap, TrendingUp, ChevronRight, Play, Bot, X,
  Eye, ExternalLink, Clock
} from 'lucide-react';
import { useModals } from '@/context/ModalContext';
import NewsCard from '@/components/news/NewsCard';
import { fetchArticles } from '@/lib/api';
import type { Article } from '@/lib/api';

// Dynamic import for R3F (SSR incompatible)
const ParticleScene = dynamic(
  () => import('@/components/three/ParticleScene'),
  { ssr: false }
);

// ─── Static demo data (fallback if API unreachable) ──────
const DEMO_ARTICLES: Article[] = [
  {
    id: '1', title: 'Sensex Rallies 800 Points as FII Inflows Surge to Record High',
    slug: 'sensex-rallies', content: '',
    summary: 'Sensex surges 800+ points on record FII inflows of ₹12,500 crore, led by banking and IT stocks.',
    source_url: '', source_name: 'ET Markets', author: 'Priya Sharma',
    image_url: 'https://images.pexels.com/photos/6801648/pexels-photo-6801648.jpeg?w=800',
    category: 1, category_name: 'Markets', tags: ['sensex', 'FII'],
    reading_time_minutes: 5, views_count: 38883, likes_count: 1079,
    is_trending: true, is_breaking: true, published_at: new Date(Date.now() - 3600000).toISOString(),
  },
  {
    id: '2', title: "India's AI Startup Ecosystem Crosses $25 Billion Valuation Mark",
    slug: 'ai-startups', content: '',
    summary: "India's AI startup ecosystem surpasses $25B valuation with 3,200+ startups, led by GenAI companies.",
    source_url: '', source_name: 'ET Startups', author: 'Vikram Patel',
    image_url: 'https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?w=800',
    category: 2, category_name: 'Startups', tags: ['AI', 'startups'],
    reading_time_minutes: 8, views_count: 21043, likes_count: 1516,
    is_trending: true, is_breaking: false, published_at: new Date(Date.now() - 7200000).toISOString(),
  },
  {
    id: '3', title: 'RBI Holds Repo Rate Steady at 6.0%, Signals Accommodative Stance',
    slug: 'rbi-rate', content: '',
    summary: 'RBI holds repo rate at 6.0%, shifts to accommodative stance. GDP forecast raised to 6.8%.',
    source_url: '', source_name: 'ET Economy', author: 'Ananya Iyer',
    image_url: 'https://images.pexels.com/photos/4386476/pexels-photo-4386476.jpeg?w=800',
    category: 4, category_name: 'Economy', tags: ['RBI', 'economy'],
    reading_time_minutes: 10, views_count: 10522, likes_count: 794,
    is_trending: true, is_breaking: true, published_at: new Date(Date.now() - 10800000).toISOString(),
  },
  {
    id: '4', title: 'Google Launches Gemini 3.0 Ultra with Real-Time Reasoning Capabilities',
    slug: 'gemini-3', content: '',
    summary: "Google's Gemini 3.0 Ultra features 2M token context, real-time reasoning traces, and 92.4% GPQA score.",
    source_url: '', source_name: 'ET Tech', author: 'Rohit Kumar',
    image_url: 'https://images.pexels.com/photos/17483868/pexels-photo-17483868.jpeg?w=800',
    category: 3, category_name: 'Technology', tags: ['Google', 'AI'],
    reading_time_minutes: 6, views_count: 26205, likes_count: 427,
    is_trending: true, is_breaking: false, published_at: new Date(Date.now() - 14400000).toISOString(),
  },
  {
    id: '5', title: 'OpenAI Launches GPT-5 Turbo with Native Agent Capabilities',
    slug: 'gpt5', content: '',
    summary: 'GPT-5 Turbo features 4M token context, native agents, persistent memory. 95.1% SWE-bench score.',
    source_url: '', source_name: 'ET Tech', author: 'Aditi Krishnan',
    image_url: 'https://images.pexels.com/photos/8386434/pexels-photo-8386434.jpeg?w=800',
    category: 7, category_name: 'AI & ML', tags: ['OpenAI', 'GPT-5'],
    reading_time_minutes: 9, views_count: 38391, likes_count: 1689,
    is_trending: true, is_breaking: true, published_at: new Date(Date.now() - 18000000).toISOString(),
  },
  {
    id: '6', title: 'Infosys Wins $2 Billion AI Transformation Deal with Deutsche Bank',
    slug: 'infosys-deal', content: '',
    summary: "Infosys bags $2B deal with Deutsche Bank — largest in company history. AI transformation across banking ops.",
    source_url: '', source_name: 'ET Tech', author: 'Nikhil Kapoor',
    image_url: 'https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?w=800',
    category: 3, category_name: 'Technology', tags: ['Infosys', 'AI-deal'],
    reading_time_minutes: 7, views_count: 45682, likes_count: 1864,
    is_trending: true, is_breaking: false, published_at: new Date(Date.now() - 21600000).toISOString(),
  },
];

const FEATURES = [
  {
    icon: Sparkles,
    title: 'AI-Powered Briefings',
    description: 'Get synthesized news briefings from multiple sources, powered by Gemini and GPT.',
    color: '#dc2626',
  },
  {
    icon: Radio,
    title: 'Story Arc Tracker',
    description: 'Follow multi-day stories through interactive timelines with entity mapping.',
    color: '#e11d48',
  },
  {
    icon: BarChart3,
    title: 'Smart Personalization',
    description: 'News curated to your interests, profession, and financial goals via AI profiling.',
    color: '#b76e79',
  },
  {
    icon: Globe2,
    title: 'Vernacular Engine',
    description: 'Business news translated and culturally adapted to 8 Indian languages.',
    color: '#059669',
  },
];

// ─── Article Detail Modal ────────────────────────────────
function ArticleModal({ article, onClose }: { article: Article; onClose: () => void }) {
  return (
    <motion.div
      className="modal-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="modal-content"
        initial={{ opacity: 0, y: 40, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 20, scale: 0.98 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: 640, maxHeight: '85vh', overflowY: 'auto' }}
      >
        <button className="modal-close" onClick={onClose}>
          <X size={16} />
        </button>

        {/* Article Image */}
        <div style={{
          borderRadius: 'var(--radius-md)',
          overflow: 'hidden',
          marginBottom: 20,
          height: 220,
        }}>
          <img
            src={article.image_url}
            alt={article.title}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>

        {/* Badges */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
          <span className="badge badge-category">{article.category_name}</span>
          {article.is_breaking && (
            <span className="badge badge-breaking"><Zap size={10} /> Breaking</span>
          )}
          {article.is_trending && (
            <span className="badge badge-trending"><TrendingUp size={10} /> Trending</span>
          )}
        </div>

        <h2 style={{
          fontSize: 22,
          fontWeight: 800,
          lineHeight: 1.3,
          marginBottom: 12,
          letterSpacing: '-0.5px',
        }}>
          {article.title}
        </h2>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 16,
          fontSize: 12,
          color: 'var(--text-tertiary)',
          marginBottom: 16,
        }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <Clock size={12} /> {article.reading_time_minutes} min read
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <Eye size={12} /> {article.views_count.toLocaleString()} views
          </span>
          <span>{article.source_name}</span>
        </div>

        <p style={{
          fontSize: 15,
          lineHeight: 1.8,
          color: 'var(--text-secondary)',
          marginBottom: 20,
        }}>
          {article.summary}
        </p>

        {article.content && (
          <p style={{
            fontSize: 14,
            lineHeight: 1.8,
            color: 'var(--text-secondary)',
            marginBottom: 20,
          }}>
            {article.content}
          </p>
        )}

        {/* Tags */}
        {article.tags?.length > 0 && (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 20 }}>
            {article.tags.map((tag) => (
              <span key={tag} style={{
                padding: '3px 10px',
                borderRadius: 'var(--radius-full)',
                background: 'rgba(220, 38, 38, 0.06)',
                fontSize: 11,
                fontWeight: 500,
                color: 'var(--accent-crimson)',
              }}>
                #{tag}
              </span>
            ))}
          </div>
        )}

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          paddingTop: 16,
          borderTop: '1px solid rgba(0,0,0,0.06)',
        }}>
          <div style={{
            width: 32,
            height: 32,
            borderRadius: '50%',
            background: 'var(--gradient-primary)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 13, fontWeight: 700, color: '#fff',
          }}>
            {article.author?.charAt(0) || 'A'}
          </div>
          <div>
            <p style={{ fontSize: 13, fontWeight: 600 }}>{article.author || 'Staff Reporter'}</p>
            <p style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
              {article.source_name} · {new Date(article.published_at).toLocaleDateString()}
            </p>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default function HomePage() {
  const { setShowDemo, setShowConcierge } = useModals();
  const [articles, setArticles] = useState<Article[]>(DEMO_ARTICLES);
  const [loading, setLoading] = useState(true);
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);

  useEffect(() => {
    const loadArticles = async () => {
      try {
        const data = await fetchArticles();
        if (data?.length > 0) {
          setArticles(data);
        }
      } catch {
        // Fall back to demo data
      } finally {
        setLoading(false);
      }
    };
    loadArticles();
  }, []);

  const scrollToSection = useCallback((id: string) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, []);

  return (
    <>
      <ParticleScene />
      <div className="main-content">
        {/* ─── Hero Section ─── */}
        <section style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          paddingTop: 64,
          position: 'relative',
        }}>
          {/* Radial glow — warm crimson */}
          <div style={{
            position: 'absolute',
            top: '30%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: 800,
            height: 800,
            background: 'radial-gradient(ellipse, rgba(220,38,38,0.06) 0%, rgba(225,29,72,0.03) 40%, transparent 70%)',
            pointerEvents: 'none',
          }} />

          <div className="container" style={{ position: 'relative', zIndex: 10 }}>
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              style={{ textAlign: 'center', maxWidth: 800, margin: '0 auto' }}
            >
              {/* Eyebrow */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 10,
                  padding: '8px 16px',
                  borderRadius: 30,
                  background: 'rgba(220,38,38,0.08)',
                  border: '1px solid rgba(220,38,38,0.2)',
                  color: 'var(--accent-crimson)',
                  fontSize: 13,
                  fontWeight: 700,
                  marginBottom: 32,
                  boxShadow: '0 0 20px rgba(220,38,38,0.1)',
                }}
              >
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'currentColor' }} />
                NEXT-GEN INTELLIGENCE: LLAMA-4-SCOUT-17B
              </motion.div>

              {/* Headline */}
              <h1 style={{
                fontSize: 'clamp(48px, 8vw, 84px)',
                fontWeight: 900,
                lineHeight: 0.95,
                letterSpacing: '-3px',
                marginBottom: 24,
                color: 'var(--text-primary)',
              }}>
                Actionable <span className="text-gradient">Intelligence</span> for the Bold.
              </h1>

              {/* Subtitle */}
              <p style={{
                fontSize: 'clamp(16px, 2vw, 20px)',
                color: 'var(--text-secondary)',
                maxWidth: 600,
                margin: '0 auto 48px',
                lineHeight: 1.6,
              }}>
                NewsAI synthesizes global market signals into high-fidelity briefings using the latest Llama-4-Scout models.
              </p>

              {/* CTAs */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}
              >
                <button
                  className="btn-primary"
                  style={{ padding: '14px 32px', fontSize: 16 }}
                  onClick={() => scrollToSection('trending')}
                >
                  Explore Now
                </button>
                <button
                  className="btn-ghost"
                  style={{ padding: '14px 28px', fontSize: 15 }}
                  onClick={() => setShowDemo(true)}
                >
                  <Play size={16} />
                  Watch Demo
                </button>
              </motion.div>

              {/* Stats */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.9 }}
                style={{
                  display: 'flex',
                  justifyContent: 'center',
                  gap: 48,
                  marginTop: 60,
                  flexWrap: 'wrap',
                }}
              >
                {[
                  { value: `${articles.length}+`, label: 'Live Articles' },
                  { value: '8', label: 'Categories' },
                  { value: '3', label: 'Story Arcs' },
                  { value: 'AI', label: 'Concierge Ready' },
                ].map((stat) => (
                  <div key={stat.label} style={{ textAlign: 'center' }}>
                    <div className="text-gradient" style={{ fontSize: 32, fontWeight: 800 }}>
                      {stat.value}
                    </div>
                    <div style={{ fontSize: 13, color: 'var(--text-tertiary)', marginTop: 4 }}>
                      {stat.label}
                    </div>
                  </div>
                ))}
              </motion.div>
            </motion.div>
          </div>

          {/* Scroll indicator */}
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            style={{
              position: 'absolute',
              bottom: 40,
              left: '50%',
              transform: 'translateX(-50%)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 8,
              color: 'var(--text-tertiary)',
              fontSize: 12,
              cursor: 'pointer',
            }}
            onClick={() => scrollToSection('features')}
          >
            <span>Scroll to explore</span>
            <ChevronRight size={16} style={{ transform: 'rotate(90deg)' }} />
          </motion.div>
        </section>

        {/* ─── Features Section ─── */}
        <section id="features" style={{ padding: '80px 0' }}>
          <div className="container">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              style={{ textAlign: 'center', marginBottom: 60 }}
            >
              <h2 style={{ fontSize: 36, fontWeight: 800, marginBottom: 16, letterSpacing: '-1px' }}>
                Six <span className="text-gradient">AI Engines</span>, One Platform
              </h2>
              <p style={{ color: 'var(--text-secondary)', fontSize: 16, maxWidth: 560, margin: '0 auto' }}>
                Every feature is powered by LLM synthesis, semantic search, and intelligent personalization.
              </p>
            </motion.div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: 20,
            }}>
              {FEATURES.map((feature, i) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1, duration: 0.5 }}
                  className="glass-card"
                  style={{ padding: 28 }}
                >
                  <div style={{
                    width: 48,
                    height: 48,
                    borderRadius: 14,
                    background: `${feature.color}12`,
                    border: `1px solid ${feature.color}25`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: 20,
                  }}>
                    <feature.icon size={22} style={{ color: feature.color }} />
                  </div>
                  <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>{feature.title}</h3>
                  <p style={{ fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.7 }}>
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* ─── News Grid Section ─── */}
        <section id="trending" style={{ padding: '40px 0 80px' }}>
          <div className="container">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 32,
              }}
            >
              <div>
                <h2 style={{ fontSize: 32, fontWeight: 800, letterSpacing: '-1px' }}>
                  <TrendingUp size={28} style={{ display: 'inline', color: 'var(--accent-crimson)', marginRight: 12 }} />
                  Trending Now
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginTop: 4 }}>
                  AI-curated top stories from across the business world
                </p>
              </div>
              <button
                className="btn-ghost"
                onClick={() => scrollToSection('trending')}
              >
                View All <ArrowRight size={14} />
              </button>
            </motion.div>

            <div className="grid-news">
              {articles.slice(0, 1).map((article, i) => (
                <NewsCard
                  key={article.id}
                  article={article}
                  index={i}
                  featured
                  onClick={() => setSelectedArticle(article)}
                />
              ))}
              {articles.slice(1, 7).map((article, i) => (
                <NewsCard
                  key={article.id}
                  article={article}
                  index={i + 1}
                  onClick={() => setSelectedArticle(article)}
                />
              ))}
            </div>
          </div>
        </section>

        {/* ─── CTA Section ─── */}
        <section id="concierge" style={{ padding: '80px 0 120px' }}>
          <div className="container">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="glass-card"
              style={{
                padding: '60px 40px',
                textAlign: 'center',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              {/* Glow effect */}
              <div style={{
                position: 'absolute',
                top: '-50%',
                left: '50%',
                transform: 'translateX(-50%)',
                width: 600,
                height: 600,
                background: 'radial-gradient(ellipse, rgba(220,38,38,0.06) 0%, transparent 60%)',
                pointerEvents: 'none',
              }} />

              <div style={{ position: 'relative' }}>
                <Bot size={48} style={{ color: 'var(--accent-rose)', marginBottom: 24 }} />
                <h2 style={{ fontSize: 36, fontWeight: 800, marginBottom: 16, letterSpacing: '-1px' }}>
                  Meet Your <span className="text-gradient">AI Concierge</span>
                </h2>
                <p style={{
                  color: 'var(--text-secondary)',
                  fontSize: 16,
                  maxWidth: 500,
                  margin: '0 auto 32px',
                  lineHeight: 1.7,
                }}>
                  A 3-minute conversation that personalizes your entire news experience.
                  Voice-enabled, multilingual, and always learning.
                </p>
                <button
                  className="btn-primary"
                  style={{ padding: '14px 32px', fontSize: 15 }}
                  onClick={() => setShowConcierge(true)}
                >
                  <Bot size={16} />
                  Start Conversation
                </button>
              </div>
            </motion.div>
          </div>
        </section>

        {/* ─── Footer ─── */}
        <footer style={{
          borderTop: '1px solid rgba(0,0,0,0.06)',
          padding: '40px 0',
        }}>
          <div className="container" style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
            <p style={{ fontSize: 13, color: 'var(--text-tertiary)' }}>
              © 2026 NewsAI. AI-Native Business Intelligence Platform.
            </p>
            <div style={{ display: 'flex', gap: 24, fontSize: 13, color: 'var(--text-tertiary)' }}>
              <span>Django 5.x</span>
              <span>Next.js 14</span>
              <span>Gemini + Groq</span>
              <span>React Three Fiber</span>
            </div>
          </div>
        </footer>
      </div>

      {/* ─── Modals ─── */}
      <AnimatePresence mode="wait">
        {selectedArticle && (
          <ArticleModal
            key="article-modal"
            article={selectedArticle}
            onClose={() => setSelectedArticle(null)}
          />
        )}
      </AnimatePresence>
    </>
  );
}
