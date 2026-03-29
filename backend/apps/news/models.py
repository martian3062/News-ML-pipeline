"""
News & Article models — core content layer.
"""
from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#6366f1")

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Core news article model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    content = models.TextField()
    summary = models.TextField(blank=True)
    source_url = models.URLField(max_length=1000, blank=True)
    source_name = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="articles")
    tags = models.JSONField(default=list, blank=True)

    # AI-generated metadata
    entities = models.JSONField(default=list, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    reading_level = models.CharField(max_length=20, blank=True)
    reading_time_minutes = models.IntegerField(default=5)

    # Engagement
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    is_trending = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)

    published_at = models.DateTimeField(null=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["source_name"]),
            models.Index(fields=["is_processed"]),
            models.Index(fields=["is_trending"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:500]
            # Ensure uniqueness
            if Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ReadingHistory(models.Model):
    """Tracks user article reading for personalization."""
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reading_history")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    time_spent_seconds = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-read_at"]
        unique_together = ["user", "article"]
