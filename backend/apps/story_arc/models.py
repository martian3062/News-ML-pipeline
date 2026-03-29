import uuid
from django.db import models


class StoryArc(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    entities = models.JSONField(default=list)
    articles = models.ManyToManyField("news.Article", related_name="story_arcs", blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class TimelineEvent(models.Model):
    story_arc = models.ForeignKey(StoryArc, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=300)
    description = models.TextField()
    event_date = models.DateTimeField()
    sentiment = models.FloatField(default=0.0)
    importance = models.IntegerField(default=5)
    source_article = models.ForeignKey("news.Article", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-event_date"]
