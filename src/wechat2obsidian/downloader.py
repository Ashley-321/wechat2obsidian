"""Download images from WeChat CDN with anti-hotlink bypass."""
import hashlib
import os
import re

import requests

IMG_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://mp.weixin.qq.com/",
}

# Only download images from these domains
ALLOWED_DOMAINS = ("mmbiz.qpic.cn", "mmbiz.qlogo.cn")


def extract_image_urls(content_soup):
    """Extract all image URLs from the content soup.

    Returns:
        list of (original_url, data_src_url) tuples.
        data_src is WeChat's lazy-load attribute.
    """
    urls = []
    for img in content_soup.find_all("img"):
        data_src = img.get("data-src") or img.get("src")
        if data_src and any(d in data_src for d in ALLOWED_DOMAINS):
            urls.append(data_src)
    return urls


def get_image_filename(url):
    """Generate a local filename for an image URL.

    Uses MD5 hash of URL for uniqueness.
    Format: wechat_{hash12}.{ext}
    """
    # Extract format from wx_fmt parameter
    fmt_match = re.search(r"wx_fmt=(\w+)", url)
    ext = fmt_match.group(1) if fmt_match else "png"
    if ext == "jpeg":
        ext = "jpg"
    # Handle SVG
    if ext == "svg":
        ext = "svg"

    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
    return "wechat_{}.{}".format(url_hash, ext)


def download_image(url, save_dir, timeout=30, retries=2):
    """Download a single image and save to save_dir.

    Args:
        url: Image URL
        save_dir: Directory to save the image
        timeout: Request timeout in seconds
        retries: Number of retry attempts on failure

    Returns:
        Local filename on success, None on failure
    """
    filename = get_image_filename(url)
    filepath = os.path.join(save_dir, filename)

    # Skip if already downloaded
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return filename

    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=IMG_HEADERS, timeout=timeout, stream=True)
            if resp.status_code == 200:
                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        f.write(chunk)
                return filename
            else:
                if attempt < retries:
                    time.sleep(1)
                    continue
                print("    HTTP {}: {}".format(resp.status_code, url[:60]))
                return None
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            print("    Error: {} - {}".format(str(e)[:40], url[:60]))
            return None


def download_all_images(image_urls, save_dir, delay=0.3):
    """Download all images, returning a mapping of URL -> local filename.

    Args:
        image_urls: list of image URLs
        save_dir: directory to save images
        delay: seconds between requests

    Returns:
        dict mapping original URL to local filename
    """
    import time

    os.makedirs(save_dir, exist_ok=True)
    img_map = {}
    total = len(image_urls)

    for i, url in enumerate(image_urls, 1):
        local_name = download_image(url, save_dir)
        if local_name:
            img_map[url] = local_name
            size_kb = os.path.getsize(os.path.join(save_dir, local_name)) / 1024
            print("  [{}/{}] {} ({:.1f}KB)".format(i, total, local_name, size_kb))
        else:
            print("  [{}/{}] FAILED".format(i, total))

        if i < total and delay > 0:
            time.sleep(delay)

    return img_map
