import uuid
from django.db import models
from django.conf import settings


class ConversationSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    messages = models.JSONField(default=list)
    profile_extracted = models.JSONField(default=dict, blank=True)
    products_recommended = models.JSONField(default=list, blank=True)
    session_type = models.CharField(
        max_length=20,
        choices=[
            ("onboarding", "Onboarding"),
            ("marketplace", "Marketplace"),
            ("support", "Support"),
        ],
        default="onboarding",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"Session {self.id} ({self.session_type})"
