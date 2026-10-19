from urllib.parse import urlparse

from ddgs import DDGS
from ddgs.exceptions import DDGSException


class WebSearchError(RuntimeError):
    """Raised when the external search provider cannot complete a lookup."""


def search_web(query, max_results=4):
    """Search DuckDuckGo and return a small set of safe, displayable results."""
    try:
        results = DDGS(timeout=8).text(
            query,
            region="wt-wt",
            safesearch="moderate",
            max_results=max_results,
            backend="duckduckgo",
        )
    except DDGSException as error:
        raise WebSearchError(f"DuckDuckGo lookup failed: {error}") from error

    sources = []
    for result in results:
        url = result.get("href")
        if not isinstance(url, str):
            continue
        url = url.strip()
        parsed_url = urlparse(url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            continue

        title = result.get("title")
        snippet = result.get("body")
        if not isinstance(title, str) or not isinstance(snippet, str):
            continue
        title = title.strip()
        snippet = snippet.strip()
        if not title or not snippet:
            continue

        sources.append({
            "title": title[:250],
            "url": url,
            "text": snippet[:1200],
            "type": "web",
        })

    return sources
