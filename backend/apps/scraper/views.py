import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .spiders.bs4_spider import BS4Spider
from apps.news.models import Article

logger = logging.getLogger(__name__)

class ScrapeView(APIView):
    """
    POST /api/scraper/scrape/
    Accepts: {"url": "...", "source": "..."}
    Returns: {"message": "...", "article_id": 123}
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        url = request.data.get("url")
        source = request.data.get("source", "Manual Scrape")

        if not url:
            return Response({"error": "url is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            spider = BS4Spider(source_name=source, base_url=url)
            scraped = spider.extract_article(url)

            if not scraped:
                return Response({"error": "Failed to extract content."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Save to Database
            article, created = Article.objects.get_or_create(
                source_url=scraped.url,
                defaults={
                    "title": scraped.title,
                    "content": scraped.content,
                    "author": scraped.author or "Unknown",
                    "source_name": scraped.source,
                }
            )

            return Response({
                "message": "Scraped successfully.",
                "article_id": article.id,
                "title": article.title,
                "created": created
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"ScrapeView Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
