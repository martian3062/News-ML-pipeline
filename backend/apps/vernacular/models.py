import uuid
from django.db import models


class Translation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_article = models.ForeignKey("news.Article", on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=5)
    translated_title = models.CharField(max_length=500)
    translated_content = models.TextField()
    translated_summary = models.TextField(blank=True)
    quality_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["source_article", "language"]

    def __str__(self):
        return f"{self.translated_title} ({self.language})"


SUPPORTED_LANGUAGES = [
    ("hi", "Hindi"), ("ta", "Tamil"), ("te", "Telugu"),
    ("bn", "Bengali"), ("mr", "Marathi"), ("gu", "Gujarati"),
    ("kn", "Kannada"), ("ml", "Malayalam"),
]
