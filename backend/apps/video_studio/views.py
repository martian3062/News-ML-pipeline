import os
import logging
import re
from django.conf import settings
from django.http import StreamingHttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.news.models import Article
from apps.video_studio.pipeline import generate_news_video

from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class GenerateVideoView(APIView):
    """
    POST /api/video-studio/generate/
    Accepts: {"article_slug": "..."}
    Returns: {"video_url": "/api/video-studio/stream/news_video_....mp4"}
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        article_slug = request.data.get("article_slug")
        if not article_slug:
            return Response({"error": "article_slug is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            # Fallback: Create a virtual/demo article if slug is 'isro-one' or similar
            slug_lower = (article_slug or "").lower()
            if "isro" in slug_lower or "isoro" in slug_lower:
                from django.utils.timezone import now
                from apps.news.models import Category
                tech_cat, _ = Category.objects.get_or_create(name="Technology", defaults={"slug": "technology"})
                article = Article.objects.create(
                    title="ISRO's Historic Mission: One for the Ages",
                    slug=article_slug,
                    content="The Indian Space Research Organisation (ISRO) has achieved a new milestone in space exploration. This mission represents a significant leap forward for autonomous space operations and deep space communication.",
                    summary="ISRO achieves historic milestone in autonomous space mission.",
                    source_name="NewsAI Demo",
                    category=tech_cat,
                    published_at=now()
                )
                logger.info(f"Created virtual demo article for slug: {article_slug}")
            else:
                return Response({"error": f"Article with slug '{article_slug}' not found. Please provide a valid slug."}, status=status.HTTP_404_NOT_FOUND)
            
        # Check if a video for this article already exists
        videos_dir = os.path.join(settings.MEDIA_ROOT, "videos")
        if os.path.exists(videos_dir):
            for file in os.listdir(videos_dir):
                if file.startswith(f"news_video_{article_slug}") and file.endswith(".mp4"):
                    # Point to the streaming endpoint instead of direct media URL
                    video_url = f"/api/video-studio/stream/{file}"
                    logger.info(f"Returning existing video for {article_slug}: {video_url}")
                    return Response({
                        "message": "Existing video found.",
                        "video_url": video_url,
                        "cached": True
                    }, status=status.HTTP_200_OK)

        # Synchronously generate the video
        logger.info(f"API Triggered: Generating video for {article_slug}...")
        try:
            video_path = generate_news_video(article_slug)
            if not video_path:
                return Response({"error": "Video pipeline failed to generate media."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            filename = os.path.basename(video_path)
            # Use streaming endpoint
            video_url = f"/api/video-studio/stream/{filename}"
            
            return Response({
                "message": "Video generated successfully.",
                "video_url": video_url,
                "cached": False
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"GenerateVideoView Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VideoStreamView(APIView):
    """
    GET /api/video-studio/stream/<filename>/
    Handles Range requests for video seeking.
    """
    def get(self, request, filename, *args, **kwargs):
        path = os.path.join(settings.MEDIA_ROOT, "videos", filename)
        if not os.path.exists(path):
            return Response(status=status.HTTP_404_NOT_FOUND)

        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        size = os.path.getsize(path)
        content_type = 'video/mp4'

        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = int(last_byte) if last_byte else size - 1
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            
            def file_iterator():
                with open(path, 'rb') as f:
                    f.seek(first_byte)
                    remaining = length
                    while remaining > 0:
                        chunk_size = min(remaining, 8192)
                        data = f.read(chunk_size)
                        if not data:
                            break
                        yield data
                        remaining -= len(data)

            resp = StreamingHttpResponse(file_iterator(), status=206, content_type=content_type)
            resp['Content-Range'] = 'bytes %d-%d/%d' % (first_byte, last_byte, size)
        else:
            resp = FileResponse(open(path, 'rb'), content_type=content_type)
            resp['Content-Length'] = str(size)

        resp['Accept-Ranges'] = 'bytes'
        return resp
