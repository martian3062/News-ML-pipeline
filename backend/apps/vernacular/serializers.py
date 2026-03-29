from rest_framework import serializers
from .models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    original_title = serializers.CharField(source="source_article.title", read_only=True)

    class Meta:
        model = Translation
        fields = ["id", "source_article", "original_title", "language",
                  "translated_title", "translated_content", "translated_summary",
                  "quality_score", "created_at"]
