'use client';

import { motion } from 'framer-motion';
import { Clock, Eye, Heart, TrendingUp, Zap } from 'lucide-react';
import type { Article } from '@/lib/api';

function timeAgo(dateStr: string): string {
  const now = new Date();
  const date = new Date(dateStr);
  const diffMs = now.getTime() - date.getTime();
  const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
  if (diffHrs < 1) return 'Just now';
  if (diffHrs < 24) return `${diffHrs}h ago`;
  const diffDays = Math.floor(diffHrs / 24);
  return `${diffDays}d ago`;
}

function formatCount(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return n.toString();
}

export default function NewsCard({
  article,
  index = 0,
  featured = false,
  onClick,
}: {
  article: Article;
  index?: number;
  featured?: boolean;
  onClick?: () => void;
}) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.05, ease: [0.25, 0.46, 0.45, 0.94] }}
      className="glass-card"
      onClick={onClick}
      style={{
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        ...(featured && {
          gridColumn: 'span 2',
          flexDirection: 'row' as const,
        }),
      }}
    >
      {/* Image */}
      <div style={{
        position: 'relative',
        overflow: 'hidden',
        ...(featured
          ? { width: '45%', minHeight: 300 }
          : { height: 200, width: '100%' }),
        borderRadius: featured ? 'var(--radius-lg) 0 0 var(--radius-lg)' : 'var(--radius-lg) var(--radius-lg) 0 0',
      }}>
        <img
          src={article.image_url}
          alt={article.title}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transition: 'transform 0.5s ease',
          }}
          onMouseEnter={(e) => { e.currentTarget.style.transform = 'scale(1.05)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)'; }}
        />

        {/* Gradient overlay — light version */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(to top, rgba(250,247,245,0.7) 0%, transparent 60%)',
        }} />

        {/* Badges */}
        <div style={{ position: 'absolute', top: 12, left: 12, display: 'flex', gap: 6 }}>
          {article.is_breaking && (
            <span className="badge badge-breaking">
              <Zap size={10} /> Breaking
            </span>
          )}
          {article.is_trending && !article.is_breaking && (
            <span className="badge badge-trending">
              <TrendingUp size={10} /> Trending
            </span>
          )}
        </div>

        {/* Category on image */}
        <div style={{ position: 'absolute', bottom: 12, left: 12 }}>
          <span className="badge badge-category">{article.category_name}</span>
        </div>
      </div>

      {/* Content */}
      <div style={{
        padding: featured ? '24px 28px' : '16px 20px',
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        justifyContent: 'space-between',
      }}>
        <div>
          <h3 style={{
            fontSize: featured ? 22 : 16,
            fontWeight: 700,
            lineHeight: 1.4,
            marginBottom: 8,
            display: '-webkit-box',
            WebkitLineClamp: featured ? 3 : 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
            color: 'var(--text-primary)',
          }}>
            {article.title}
          </h3>

          <p style={{
            fontSize: 13,
            color: 'var(--text-secondary)',
            lineHeight: 1.6,
            display: '-webkit-box',
            WebkitLineClamp: featured ? 4 : 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
            marginBottom: 16,
          }}>
            {article.summary}
          </p>
        </div>

        {/* Meta row */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          paddingTop: 12,
          borderTop: '1px solid rgba(0,0,0,0.06)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            {/* Author avatar */}
            <div style={{
              width: 28,
              height: 28,
              borderRadius: '50%',
              background: 'var(--gradient-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 11,
              fontWeight: 700,
              color: '#ffffff',
            }}>
              {article.author?.charAt(0) || 'A'}
            </div>
            <div>
              <p style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-primary)' }}>
                {article.author || 'Staff'}
              </p>
              <p style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
                {article.source_name} · {timeAgo(article.published_at)}
              </p>
            </div>
          </div>

          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            fontSize: 11,
            color: 'var(--text-tertiary)',
          }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
              <Eye size={12} /> {formatCount(article.views_count)}
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
              <Heart size={12} /> {formatCount(article.likes_count)}
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 3 }}>
              <Clock size={12} /> {article.reading_time_minutes}m
            </span>
          </div>
        </div>
      </div>
    </motion.article>
  );
}
