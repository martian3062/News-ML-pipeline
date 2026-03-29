from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Article
from .serializers import CategorySerializer, ArticleListSerializer, ArticleDetailSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.select_related("category").all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category__slug", "source_name", "is_trending", "is_breaking"]
    search_fields = ["title", "content", "summary", "tags"]
    ordering_fields = ["published_at", "views_count", "likes_count"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleDetailSerializer
        return ArticleListSerializer

    @action(detail=False, methods=["get"])
    def trending(self, request):
        trending = self.queryset.filter(is_trending=True)[:10]
        serializer = ArticleListSerializer(trending, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def breaking(self, request):
        breaking = self.queryset.filter(is_breaking=True)[:5]
        serializer = ArticleListSerializer(breaking, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        """Get articles grouped by category."""
        categories = Category.objects.all()
        result = {}
        for cat in categories:
            articles = Article.objects.filter(category=cat).order_by("-published_at")[:5]
            result[cat.slug] = {
                "name": cat.name,
                "color": cat.color,
                "articles": ArticleListSerializer(articles, many=True).data,
            }
        return Response(result)
