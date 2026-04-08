"""Fetch WeChat article HTML and extract metadata + content."""
import re
import requests
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://mp.weixin.qq.com/",
}


class ArticleData(object):
    """Holds parsed article metadata and content soup."""

    def __init__(self, url, title, author, publish_time, content_soup, raw_html):
        self.url = url
        self.title = title
        self.author = author
        self.publish_time = publish_time
        self.content_soup = content_soup
        self.raw_html = raw_html


def fetch_article(url, timeout=30):
    """Fetch a WeChat article and return an ArticleData object.

    Args:
        url: WeChat article URL (mp.weixin.qq.com/s/...)
        timeout: Request timeout in seconds

    Returns:
        ArticleData object

    Raises:
        ValueError: if URL is not a valid WeChat article
        requests.RequestException: on network errors
    """
    if "mp.weixin.qq.com" not in url:
        raise ValueError(
            "Not a WeChat article URL. Expected mp.weixin.qq.com/..."
        )

    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    html = resp.text

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    # Extract title
    title = "Untitled"
    title_tag = soup.find("h1", class_="rich_media_title")
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        # Fallback: og:title meta tag
        og_title = soup.find("meta", property="og:title")
        if og_title:
            title = og_title.get("content", "Untitled")

    # Extract author
    author = "Unknown"
    author_tag = soup.find("a", class_="rich_media_meta_link")
    if author_tag:
        author = author_tag.get_text(strip=True)
    else:
        author_tag2 = soup.find(id="js_name")
        if author_tag2:
            author = author_tag2.get_text(strip=True)

    # Extract publish time
    publish_time = "Unknown"
    time_tag = soup.find("span", id="publish_time")
    if time_tag:
        publish_time = time_tag.get_text(strip=True)
    else:
        time_match = re.search(r'var\s+publish_time\s*=\s*"([^"]+)"', html)
        if time_match:
            publish_time = time_match.group(1)
        else:
            # Fallback: var ct = <unix_timestamp>
            ct_match = re.search(r'var\s+ct\s*=\s*["\']?(\d{10,})', html)
            if ct_match:
                try:
                    ts = int(ct_match.group(1))
                    # Determine if seconds (10 digits) or milliseconds (13 digits)
                    if ts > 1e12:
                        ts = ts // 1000
                    publish_time = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, OSError):
                    pass

    # Extract content div
    content_div = soup.find("div", class_="rich_media_content")
    if not content_div:
        raise ValueError("Cannot find article content. The page may have changed.")

    # Remove script and style elements
    for s in content_div.find_all(["script", "style"]):
        s.decompose()

    return ArticleData(url, title, author, publish_time, content_div, html)
