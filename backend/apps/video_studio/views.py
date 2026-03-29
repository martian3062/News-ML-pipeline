import os
import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.news.models import Article
from apps.video_studio.pipeline import generate_news_video

logger = logging.getLogger(__name__)

class GenerateVideoView(APIView):
    """
    POST /api/video-studio/generate/
    Accepts: {"article_slug": "..."}
    Returns: {"video_url": "/media/videos/..."}
    """
    def post(self, request, *args, **kwargs):
        article_slug = request.data.get("article_slug")
        if not article_slug:
            return Response({"error": "article_slug is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)
            
        # Optional: Check if a video for this article already exists to prevent duplicate compute
        videos_dir = os.path.join(settings.MEDIA_ROOT, "videos")
        if os.path.exists(videos_dir):
            for file in os.listdir(videos_dir):
                if file.startswith(f"news_video_{article_slug}") and file.endswith(".mp4"):
                    video_url = f"{settings.MEDIA_URL}videos/{file}"
                    logger.info(f"Returning existing video for {article_slug}: {video_url}")
                    return Response({
                        "message": "Existing video found.",
                        "video_url": video_url,
                        "cached": True
                    }, status=status.HTTP_200_OK)

        # Synchronously generate the video (takes ~30-60s)
        logger.info(f"API Triggered: Generating video for {article_slug}...")
        try:
            video_path = generate_news_video(article_slug)
            if not video_path:
                return Response({"error": "Video pipeline failed to generate media."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            # Convert absolute path to relative media URL
            filename = os.path.basename(video_path)
            video_url = f"{settings.MEDIA_URL}videos/{filename}"
            
            return Response({
                "message": "Video generated successfully.",
                "video_url": video_url,
                "cached": False
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"GenerateVideoView Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
