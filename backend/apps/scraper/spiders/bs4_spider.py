"""
BeautifulSoup4 scraper for static news pages.
"""
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ScrapedArticle:
    url: str
    title: str
    content: str
    author: Optional[str] = None
    published_date: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    source: str = "Unknown"

class BS4Spider:
    """Scrapes static HTML news pages using requests + BeautifulSoup4."""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def extract_article(self, url: str) -> Optional[ScrapedArticle]:
        soup = self.fetch_page(url)
        if not soup:
            return None

        # Generic extraction
        title = soup.find("h1")
        title_text = title.get_text(strip=True) if title else ""

        content_el = (
            soup.find("article")
            or soup.find("div", class_="article-body")
            or soup.find("div", class_="story-content")
            or soup.find("main")
        )
        content_text = content_el.get_text(separator="\n", strip=True) if content_el else ""

        author_el = soup.find("meta", attrs={"name": "author"})
        author = author_el["content"] if author_el else None

        image_el = soup.find("meta", attrs={"property": "og:image"})
        image_url = image_el["content"] if image_el else None

        return ScrapedArticle(
            url=url,
            title=title_text,
            content=content_text,
            author=author,
            image_url=image_url,
            source=self.source_name,
        )

    def extract_article_links(self, listing_url: str) -> list[str]:
        soup = self.fetch_page(listing_url)
        if not soup:
            return []

        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("/") and len(href) > 10:
                links.append(f"{self.base_url.rstrip('/')}{href}")
            elif href.startswith(self.base_url):
                links.append(href)

        return list(set(links))
