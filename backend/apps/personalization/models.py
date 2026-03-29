from django.db import models
from django.conf import settings


class UserPreference(models.Model):
    """Stores explicit user preferences for personalization."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences")
    preferred_categories = models.JSONField(default=list)
    preferred_sources = models.JSONField(default=list)
    blocked_topics = models.JSONField(default=list)
    notification_enabled = models.BooleanField(default=True)
    daily_digest_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
