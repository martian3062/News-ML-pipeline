import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

logging.basicConfig(level=logging.INFO, force=True)

from apps.video_studio.pipeline import generate_news_video

print("\n\n" + "="*50)
print("=== STARTING VIDEO GENERATION ===")
video_path = generate_news_video('isro-successfully-tests-reusable-launch-vehicle-in-orbital-return-mission')
print(f"=== VIDEO GENERATED: {video_path} ===")
print("="*50 + "\n\n")
