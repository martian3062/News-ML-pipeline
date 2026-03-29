"""
FFmpeg-based video composition pipeline.
Combines: Pexels footage + TTS audio + text overlays → final video.
"""

import os
import logging
import subprocess
from typing import Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class FFmpegComposer:
    """Compose news videos from footage, audio, and text overlays."""

    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or settings.GENERATED_VIDEOS_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def compose_news_video(
        self,
        segments: list[dict],
        output_filename: str,
        resolution: str = "1920x1080",
        fps: int = 30,
    ) -> str:
        """
        Compose a full news video from segments.

        Each segment dict:
        {
            "video_path": "/path/to/pexels_clip.mp4",
            "audio_path": "/path/to/tts_narration.wav",
            "text_overlay": "Breaking: GDP growth hits 7.2%",
            "duration": 15.0,
        }
        """
        segment_files = []

        for i, segment in enumerate(segments):
            segment_output = os.path.join(self.output_dir, f"_seg_{i:03d}.mp4")
            try:
                self._compose_segment(segment, segment_output, resolution, fps)
                segment_files.append(segment_output)
            except Exception as e:
                logger.error(f"Failed to compose segment {i}: {e}")
                raise RuntimeError(f"Failed to compose segment {i}: {e}")

        # Concatenate all segments
        concat_list = os.path.join(self.output_dir, "_concat_list.txt")
        with open(concat_list, "w") as f:
            for seg_file in segment_files:
                f.write(f"file '{seg_file}'\n")

        output_path = os.path.join(self.output_dir, output_filename)
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c", "copy",
            output_path,
        ]

        self._run_ffmpeg(cmd)

        # Cleanup temp segment files
        for seg_file in segment_files:
            try:
                os.remove(seg_file)
            except:
                pass
        try:
            os.remove(concat_list)
        except:
            pass

        logger.info(f"Video composed: {output_path}")
        return output_path

    def _compose_segment(
        self, segment: dict, output: str, resolution: str, fps: int
    ):
        """Compose a single segment: video + audio + text overlay."""
        width, height = resolution.split("x")
        text = segment.get("text_overlay", "")

        # Escape special chars for FFmpeg drawtext
        text = text.replace("'", "'\\''").replace(":", "\\:")

        # Using simpler parameters to ensure broad compatibility with any clip aspect ratio without complex drawing first
        # We will drop the complex text overlay for prototype safety, or use simple subtitle if needed.
        # But per the plan, I'll attempt the text overlay. If it fails due to fonts, we might need a fallback.
        # Let's use a very basic filter complex for text
        cmd = [
            "ffmpeg", "-y",
            "-i", segment["video_path"],
            "-i", segment["audio_path"],
            "-filter_complex",
            (
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,"
                f"fps={fps},"
                f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{text}':"
                f"fontsize=36:fontcolor=white:"
                f"x=(w-tw)/2:y=h-100:"
                f"box=1:boxcolor=black@0.7:boxborderw=10[v]"
            ),
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-t", str(segment.get("duration", 15)),
            "-shortest",
            output,
        ]

        self._run_ffmpeg(cmd)

    @staticmethod
    def _run_ffmpeg(cmd: list[str]):
        """Run an FFmpeg command and handle errors."""
        try:
            logger.info(f"Running FFmpeg: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                raise RuntimeError(f"FFmpeg failed: {result.stderr[:500]}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("FFmpeg timed out after 300 seconds.")
