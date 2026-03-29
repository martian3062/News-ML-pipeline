import os
import django
import asyncio
import logging

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.video_studio.pipeline import generate_news_video

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_e2e():
    # Use a real slug from the database
    slug = "isro-successfully-tests-reusable-launch-vehicle-in-orbital-return-mission"
    
    logger.info(f"--- STARTING E2E VIDEO GEN TEST FOR: {slug} ---")
    
    try:
        # Note: generate_news_video is synchronous but internally uses asyncio for TTS
        video_path = generate_news_video(slug)
        
        if video_path and os.path.exists(video_path):
            logger.info(f"SUCCESS! Video generated at: {video_path}")
            print(f"\n[+] E2E TEST PASSED: {video_path}")
        else:
            logger.error("FAILED: Pipeline returned None or file doesn't exist.")
    except Exception as e:
        logger.error(f"FATAL ERROR: {e}")

if __name__ == "__main__":
    test_e2e()
