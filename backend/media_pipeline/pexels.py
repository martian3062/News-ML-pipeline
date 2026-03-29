"""
Pexels API client for fetching royalty-free stock footage and images.
"""

import logging
import requests
from typing import Optional
from django.conf import settings

logger = logging.getLogger(__name__)

PEXELS_BASE_URL = "https://api.pexels.com"


class PexelsClient:
    """Fetch stock videos and photos from Pexels."""

    def __init__(self):
        self.api_key = settings.PEXELS_API_KEY
        self.headers = {"Authorization": self.api_key}

    def search_videos(
        self, query: str, per_page: int = 5, orientation: str = "landscape"
    ) -> list[dict]:
        """Search for stock videos matching a query."""
        if not self.api_key:
            logger.warning("PEXELS_API_KEY not set")
            return []

        url = f"{PEXELS_BASE_URL}/videos/search"
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": orientation,
            "size": "medium",
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for video in data.get("videos", []):
                # Get HD video file
                video_files = video.get("video_files", [])
                hd_file = next(
                    (f for f in video_files if f.get("quality") == "hd"),
                    video_files[0] if video_files else None,
                )
                if hd_file:
                    results.append({
                        "id": video["id"],
                        "url": hd_file["link"],
                        "width": hd_file.get("width"),
                        "height": hd_file.get("height"),
                        "duration": video.get("duration"),
                    })

            return results

        except requests.RequestException as e:
            logger.error(f"Pexels video search failed: {e}")
            return []

pexels_client = PexelsClient()
