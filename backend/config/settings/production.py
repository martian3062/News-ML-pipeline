import dj_database_url
from .base import *

DEBUG = False

# ─── Allowed Hosts ───────────────────────────────────────────
# Whitelist Render domain and any custom domain
ALLOWED_HOSTS = ["*"]

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
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "https://ai-news-fvca.onrender.com",
    "https://news-llm.netlify.app",
    "http://news-llm.netlify.app",
]

CORS_ALLOWED_ORIGINS = [
    "https://news-llm.netlify.app",
    "http://news-llm.netlify.app",
]
CORS_ALLOW_ALL_ORIGINS = True # Temporary for debugging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
