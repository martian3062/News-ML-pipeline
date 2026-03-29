import uuid
from django.db import models
from django.conf import settings


class VideoProject(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("generating", "Generating"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    source_article = models.ForeignKey("news.Article", on_delete=models.SET_NULL, null=True)
    script = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    video_url = models.URLField(max_length=1000, blank=True)
    thumbnail_url = models.URLField(max_length=1000, blank=True)
    duration_seconds = models.IntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
