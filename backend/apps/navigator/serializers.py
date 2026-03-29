from rest_framework import serializers
from .models import Briefing
from apps.news.serializers import ArticleListSerializer


class BriefingListSerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Briefing
        fields = ["id", "title", "slug", "topic", "summary", "image_url", "article_count", "created_at"]

    def get_article_count(self, obj):
        return obj.source_articles.count()


class BriefingDetailSerializer(serializers.ModelSerializer):
    source_articles = ArticleListSerializer(many=True, read_only=True)

    class Meta:
        model = Briefing
        fields = ["id", "title", "slug", "topic", "summary", "key_insights",
                  "source_articles", "qa_pairs", "image_url", "created_at"]
