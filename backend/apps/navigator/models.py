import uuid
from django.db import models


class Briefing(models.Model):
    """Interactive news briefing — synthesized from multiple articles."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    topic = models.CharField(max_length=200)
    summary = models.TextField()
    key_insights = models.JSONField(default=list)
    source_articles = models.ManyToManyField("news.Article", related_name="briefings", blank=True)
    qa_pairs = models.JSONField(default=list)
    image_url = models.URLField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
