"""
Video Maker Automated Pipeline.
Orchestrates: Script Generation (Gemini) -> TTS (Edge-TTS) -> Footage (Pexels) -> FFmpeg Composite.
"""

import os
import json
import logging
import asyncio
import requests
import uuid
import base64
import subprocess
import edge_tts
from django.conf import settings
from langchain_core.messages import HumanMessage
from apps.news.models import Article
from ai_core.chains import get_video_script_chain, get_video_validation_chain
from media_pipeline.pexels import pexels_client
from media_pipeline.ffmpeg_composer import FFmpegComposer

logger = logging.getLogger(__name__)

# Ensure directories exist
MEDIA_ROOT = settings.MEDIA_ROOT
VIDEOS_DIR = os.path.join(MEDIA_ROOT, "videos")
AUDIO_DIR = os.path.join(MEDIA_ROOT, "audio")
PEXELS_DIR = os.path.join(MEDIA_ROOT, "raw_footage")

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(PEXELS_DIR, exist_ok=True)


async def _generate_audio(text: str, output_path: str):
    """Generate audio for a text segment using Edge-TTS."""
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(output_path)


def download_file(url: str, output_path: str):
    """Download a file from a URL."""
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def validate_footage(video_path: str, scene_description: str) -> bool:
    """Extract a frame from the video and validate its relevance using Groq Vision."""
    frame_path = video_path.replace(".mp4", "_frame.jpg")
    try:
        # Extract 1st frame
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-vframes", "1", "-q:v", "2", frame_path],
            capture_output=True, check=True
        )
        
        with open(frame_path, "rb") as f:
            b64_image = base64.b64encode(f.read()).decode("utf-8")
        
        prompt = (
            f"You are an AI video producer. Does this image reasonably match the following scene description? "
            f"Scene: '{scene_description}'. "
            f"Be very lenient. As long as it loosely fits, answer 'YES'. "
            f"Answer perfectly with either exactly 'YES' or 'NO'."
        )
        message = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}},
        ])
        
        chain = get_video_validation_chain()
        result = chain.invoke([message])
        logger.info(f"Vision Validation for {os.path.basename(video_path)}: {result}")
        
        return "YES" in result.upper()
    except Exception as e:
        logger.error(f"Vision validation failed: {e}")
        return True # Default to accept if failing
    finally:
        if os.path.exists(frame_path):
            try:
                os.remove(frame_path)
            except:
                pass


def generate_news_video(article_slug: str):
    """
    End-to-end automated pipeline to generate a video from a news article.
    """
    logger.info(f"Starting video generation for article: {article_slug}")
    
    # 1. Fetch Article
    try:
        article = Article.objects.get(slug=article_slug)
    except Article.DoesNotExist:
        logger.error(f"Article {article_slug} not found.")
        return None

    # 2. Generate Script
    logger.info("Generating video script via LangChain + Gemini...")
    script_chain = get_video_script_chain()
    # Provide the article text and a summary
    content = f"Title: {article.title}\n\n{article.content}"
    
    try:
        script_json = script_chain.invoke({"text": content})
    except Exception as e:
        logger.error(f"Script generation failed: {e}")
        return None
        
    logger.info(f"Script generated with {len(script_json)} segments.")

    # 3. Process Segments (TTS + Footage)
    composer_segments = []
    run_id = str(uuid.uuid4())[:8]

    # Event loop for async TTS processing
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for i, segment in enumerate(script_json):
        logger.info(f"Processing segment {i+1}/{len(script_json)}...")
        
        # Audio Generation
        spoken_text = segment.get("text", "")
        audio_filename = f"audio_{run_id}_{i:03d}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        loop.run_until_complete(_generate_audio(spoken_text, audio_path))
        
        # Footage Gathering
        visual_query = segment.get("scene", "news background")
        logger.info(f"Fetching Pexels footage for: {visual_query}")
        
        videos = pexels_client.search_videos(query=visual_query, per_page=1, orientation="landscape")
        
        # Fallback query if no video found
        if not videos:
            videos = pexels_client.search_videos(query="technology news background", per_page=1)
            
        if not videos:
            logger.error(f"Failed to find any footage for segment {i}. Skipping segment.")
            continue
            
        video_url = videos[0]["url"]
        video_filename = f"footage_{run_id}_{i:03d}.mp4"
        video_path = os.path.join(PEXELS_DIR, video_filename)
        
        download_file(video_url, video_path)

        # Vision Validation Phase!
        logger.info("Initializing Groq Vision model for footage validation...")
        is_valid = validate_footage(video_path, visual_query)
        if not is_valid:
            logger.warning(f"Groq Vision rejected {video_filename} for scene: '{visual_query}'")
            # We could fetch an alternative, but for the prototype we will just use a generic fallback
            generic_videos = pexels_client.search_videos(query="technology news background", per_page=1)
            if generic_videos:
                download_file(generic_videos[0]["url"], video_path)
                logger.info("Replaced with generic background footage safely.")

        # Duration logic: Try to get duration from Pexels, fallback to segment dict, fallback to 15s
        duration = videos[0].get("duration", segment.get("duration", 8))
        
        # Create segment for composer
        composer_segments.append({
            "video_path": video_path,
            "audio_path": audio_path,
            "text_overlay": segment.get("scene", "")[:30], # Short preview of scene as overlay 
            "duration": float(duration)
        })

    loop.close()

    # 4. Composite Video
    if not composer_segments:
        logger.error("No valid segments generated.")
        return None

    logger.info("Passing segments to FFmpegComposer...")
    output_filename = f"news_video_{article_slug}_{run_id}.mp4"
    
    composer = FFmpegComposer(output_dir=VIDEOS_DIR)
    
    try:
        final_video_path = composer.compose_news_video(
            segments=composer_segments,
            output_filename=output_filename,
            resolution="1280x720", # 720p for faster prototyping
            fps=24
        )
        logger.info(f"Video generation complete! Saved at: {final_video_path}")
        return final_video_path
    except Exception as e:
        logger.error(f"Video composition failed: {e}")
        return None
