import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

// ─── Types ───────────────────────────────────────────────
export interface Category {
  id: number;
  name: string;
  slug: string;
  icon: string;
  color: string;
}

export interface Article {
  id: string;
  title: string;
  slug: string;
  content?: string;
  summary: string;
  source_url: string;
  source_name: string;
  author: string;
  image_url: string;
  category: number;
  category_name: string;
  tags: string[];
  entities?: string[];
  sentiment_score?: number;
  reading_level?: string;
  reading_time_minutes: number;
  views_count: number;
  likes_count: number;
  is_trending: boolean;
  is_breaking: boolean;
  published_at: string;
}

export interface StoryArc {
  id: string;
  title: string;
  slug: string;
  description: string;
  entities: string[];
  image_url: string;
  is_active: boolean;
}

export interface Briefing {
  id: string;
  title: string;
  slug: string;
  topic: string;
  summary: string;
  key_insights: string[];
  qa_pairs: { q: string; a: string }[];
  image_url: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// ─── API Functions ───────────────────────────────────────────
export async function fetchArticles(): Promise<Article[]> {
  const res = await api.get<PaginatedResponse<Article>>('/api/news/articles/');
  return res.data.results;
}

export async function fetchArticle(slug: string): Promise<Article> {
  const res = await api.get<Article>(`/api/news/articles/${slug}/`);
  return res.data;
}

export async function fetchCategories(): Promise<Category[]> {
  const res = await api.get<PaginatedResponse<Category>>('/api/news/categories/');
  return res.data.results;
}

export async function fetchStoryArcs(): Promise<StoryArc[]> {
  const res = await api.get<PaginatedResponse<StoryArc>>('/api/story-arc/arcs/');
  return res.data.results;
}

export async function fetchBriefings(): Promise<Briefing[]> {
  const res = await api.get<PaginatedResponse<Briefing>>('/api/navigator/briefings/');
  return res.data.results;
}

export async function sendConciergeMessage(message: string, sessionId?: string): Promise<{ response: string, session_id: string }> {
  // Use a longer timeout for LLM responses
  const res = await api.post('/api/concierge/chat/', { message, session_id: sessionId }, { timeout: 30000 });
  return res.data;
}

export default api;
