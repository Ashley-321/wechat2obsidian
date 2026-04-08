"""Write Markdown files to Obsidian vault."""
import os
import re
from datetime import datetime


def sanitize_filename(name):
    """Remove/replace characters that are invalid in filenames.

    Keeps: Chinese chars, alphanumeric, underscores, hyphens, spaces, dots, parentheses.
    """
    # Replace problematic characters
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    # Collapse multiple underscores/spaces
    name = re.sub(r"[_\s]{2,}", "_", name)
    # Trim leading/trailing underscores and spaces
    name = name.strip("_ ")
    # Limit length
    if len(name) > 200:
        name = name[:200].rstrip("_ ")
    return name if name else "Untitled"


def parse_publish_time(publish_time_str):
    """Try to parse WeChat publish time into YYYY-MM-DD format.

    Args:
        publish_time_str: raw publish time string from WeChat

    Returns:
        Date string in YYYY-MM-DD format, or original string if parsing fails
    """
    if not publish_time_str or publish_time_str == "Unknown":
        return ""

    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y年%m月%d日", "%Y/%m/%d"):
        try:
            dt = datetime.strptime(publish_time_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            continue

    return publish_time_str


def build_frontmatter(title, author, publish_time, url, tags):
    """Build YAML frontmatter string.

    Args:
        title: Article title
        author: Author / account name
        publish_time: Raw publish time string
        url: Article URL
        tags: list of tag strings

    Returns:
        YAML frontmatter block as string
    """
    date = parse_publish_time(publish_time)
    lines = ["---"]
    lines.append("title: {}".format(title))
    lines.append("author: {}".format(author))
    if date:
        lines.append("date: {}".format(date))
    if publish_time and publish_time != "Unknown":
        lines.append("publish_time: {}".format(publish_time))
    lines.append("source: {}".format(url))
    if tags:
        lines.append("tags:")
        for tag in tags:
            lines.append("  - {}".format(tag))
    lines.append("---")
    return "\n".join(lines)


def write_markdown(
    article, body_md, vault_path, folder, attach_dir_rel, tags, overwrite=False
):
    """Write the final Markdown file to the vault.

    Args:
        article: ArticleData object
        body_md: Body content in Markdown (without frontmatter)
        vault_path: Absolute path to Obsidian vault
        folder: Subfolder within vault (empty string for root)
        attach_dir_rel: Relative path of attachment dir from vault root
        tags: list of tag strings
        overwrite: If True, overwrite existing files

    Returns:
        Absolute path of the written file
    """
    # Determine target directory
    if folder:
        target_dir = os.path.join(vault_path, folder)
    else:
        target_dir = vault_path

    os.makedirs(target_dir, exist_ok=True)

    # Build filename from title
    filename = sanitize_filename(article.title) + ".md"
    filepath = os.path.join(target_dir, filename)

    # Handle filename collision
    if os.path.exists(filepath) and not overwrite:
        base = sanitize_filename(article.title)
        counter = 2
        while os.path.exists(filepath):
            filename = "{}_{}.md".format(base, counter)
            filepath = os.path.join(target_dir, filename)
            counter += 1

    # Build frontmatter
    frontmatter = build_frontmatter(
        article.title, article.author, article.publish_time, article.url, tags
    )

    # Assemble final content
    content = "{}\n\n# {}\n\n{}\n".format(frontmatter, article.title, body_md)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath
