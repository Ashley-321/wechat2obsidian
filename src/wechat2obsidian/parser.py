"""Convert WeChat article HTML to Markdown."""
from bs4 import BeautifulSoup
import re


def html_to_markdown(element, img_map=None):
    """Recursively convert HTML element to Markdown string.

    Args:
        element: BeautifulSoup element
        img_map: dict mapping original image URL to local filename

    Returns:
        Markdown string
    """
    if img_map is None:
        img_map = {}

    if element is None:
        return ""

    result = []

    for child in element.children:
        if isinstance(child, str):
            text = child.strip()
            if text:
                result.append(text)
            continue

        tag = child.name

        if tag in ("script", "style"):
            continue

        # Image
        if tag == "img":
            data_src = child.get("data-src") or child.get("src")
            if data_src and data_src in img_map:
                local_name = img_map[data_src]
                # Use alt text if available
                alt = child.get("alt", "")
                if alt:
                    result.append("\n\n![{}]({})\n\n".format(alt, local_name))
                else:
                    result.append("\n\n![]({})\n\n".format(local_name))
            continue

        # Paragraph
        if tag == "p":
            inner = html_to_markdown(child, img_map)
            if inner.strip():
                result.append("\n\n{}\n\n".format(inner.strip()))
            continue

        # Line break
        if tag == "br":
            result.append("\n")
            continue

        # Bold
        if tag in ("strong", "b"):
            inner = html_to_markdown(child, img_map)
            result.append("**{}**".format(inner))
            continue

        # Italic
        if tag in ("em", "i"):
            inner = html_to_markdown(child, img_map)
            result.append("*{}*".format(inner))
            continue

        # Link
        if tag == "a":
            href = child.get("href", "")
            inner = html_to_markdown(child, img_map)
            result.append("[{}]({})".format(inner, href))
            continue

        # Headings
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            inner = html_to_markdown(child, img_map)
            result.append("\n\n{} {}\n\n".format("#" * level, inner.strip()))
            continue

        # Blockquote
        if tag == "blockquote":
            inner = html_to_markdown(child, img_map)
            lines = inner.strip().split("\n")
            quoted = "\n".join("> {}".format(line) for line in lines)
            result.append("\n\n{}\n\n".format(quoted))
            continue

        # Unordered list
        if tag == "ul":
            inner = html_to_markdown(child, img_map)
            lines = inner.strip().split("\n")
            for line in lines:
                line = line.strip()
                if line:
                    result.append("\n- {}\n".format(line))
            continue

        # Ordered list
        if tag == "ol":
            inner = html_to_markdown(child, img_map)
            lines = inner.strip().split("\n")
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line:
                    result.append("\n{}. {}\n".format(i, line))
            continue

        # List item
        if tag == "li":
            inner = html_to_markdown(child, img_map)
            result.append(inner)
            continue

        # Table (basic support)
        if tag == "table":
            inner = html_to_markdown(child, img_map)
            result.append("\n\n{}\n\n".format(inner.strip()))
            continue

        # Table header
        if tag == "th":
            inner = html_to_markdown(child, img_map)
            result.append("| {} ".format(inner.strip()))
            continue

        # Table cell
        if tag == "td":
            inner = html_to_markdown(child, img_map)
            result.append("| {} ".format(inner.strip()))
            continue

        # Table row
        if tag == "tr":
            inner = html_to_markdown(child, img_map)
            result.append(inner.strip() + "|\n")
            continue

        # Section and div (WeChat uses these as wrappers)
        if tag in ("section", "div"):
            inner = html_to_markdown(child, img_map)
            if inner.strip():
                result.append("\n\n{}\n\n".format(inner.strip()))
            continue

        # Span (inline wrapper)
        if tag == "span":
            inner = html_to_markdown(child, img_map)
            result.append(inner)
            continue

        # Code
        if tag in ("code", "pre"):
            inner = html_to_markdown(child, img_map)
            if tag == "pre":
                result.append("\n\n```\n{}\n```\n\n".format(inner.strip()))
            else:
                result.append("`{}`".format(inner))
            continue

        # Default: recurse
        inner = html_to_markdown(child, img_map)
        if inner.strip():
            result.append(inner)

    return "".join(result)


def clean_markdown(md_text):
    """Clean up excessive blank lines and whitespace."""
    # Collapse 3+ newlines to 2
    md_text = re.sub(r"\n{3,}", "\n\n", md_text)
    # Remove trailing spaces on lines
    md_text = re.sub(r" +\n", "\n", md_text)
    return md_text.strip()
