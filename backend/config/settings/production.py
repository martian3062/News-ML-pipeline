import dj_database_url
from .base import *

DEBUG = False

# ─── Allowed Hosts ───────────────────────────────────────────
# Whitelist Render domain and any custom domain
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# ─── Database ───────────────────────────────────────────────
# Use Render's DATABASE_URL for PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default=''),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ─── CSRF/Security ───────────────────────────────────────────
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "https://ai-news-fvca.onrender.com",
    "https://news-llm.netlify.app",
]

CORS_ALLOWED_ORIGINS = [
    "https://news-llm.netlify.app",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]
