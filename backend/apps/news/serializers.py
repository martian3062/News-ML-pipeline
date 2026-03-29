from rest_framework import serializers
from .models import Category, Article


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "color", "article_count"]

    def get_article_count(self, obj):
        return obj.articles.count()


class ArticleListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", default="")

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "summary", "source_name", "author",
            "image_url", "category", "category_name", "tags",
            "reading_time_minutes", "views_count", "likes_count",
            "is_trending", "is_breaking", "published_at",
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", default="")

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "content", "summary", "source_url",
            "source_name", "author", "image_url", "category", "category_name",
            "tags", "entities", "sentiment_score", "reading_level",
            "reading_time_minutes", "views_count", "likes_count",
            "is_trending", "is_breaking", "published_at", "scraped_at",
        ]
