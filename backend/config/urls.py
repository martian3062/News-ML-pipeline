"""URL configuration for AI News Platform."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/news/", include("apps.news.urls")),
    path("api/personalization/", include("apps.personalization.urls")),
    path("api/navigator/", include("apps.navigator.urls")),
    path("api/video-studio/", include("apps.video_studio.urls")),
    path("api/story-arc/", include("apps.story_arc.urls")),
    path("api/vernacular/", include("apps.vernacular.urls")),
    path("api/concierge/", include("apps.concierge.urls")),
    path("api/scraper/", include("apps.scraper.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
