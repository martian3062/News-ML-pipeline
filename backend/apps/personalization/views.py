from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from apps.news.models import Article
from apps.news.serializers import ArticleListSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def personalized_feed(request):
    """Get personalized news feed based on user preferences."""
    if request.user.is_authenticated and request.user.interests:
        # Filter by user interests
        interests = request.user.interests
        articles = Article.objects.filter(
            tags__overlap=interests
        ).order_by("-published_at")[:20]

        if not articles.exists():
            articles = Article.objects.order_by("-published_at")[:20]
    else:
        articles = Article.objects.order_by("-published_at")[:20]

    serializer = ArticleListSerializer(articles, many=True)
    return Response({
        "feed": serializer.data,
        "personalized": request.user.is_authenticated,
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def trending_topics(request):
    """Get trending topics across all articles."""
    trending = Article.objects.filter(is_trending=True).order_by("-views_count")[:10]
    serializer = ArticleListSerializer(trending, many=True)
    return Response(serializer.data)
