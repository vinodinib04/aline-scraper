import httpx
from bs4 import BeautifulSoup
from readability import Document
import markdownify
from urllib.parse import urljoin, urlparse

async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text

async def scrape_page(url: str) -> dict:
    """Scrape one page: extract title + main content → markdown"""
    html = await fetch_html(url)
    doc = Document(html)
    title = doc.short_title()
    content_html = doc.summary(html_partial=True)
    markdown = markdownify.markdownify(content_html, heading_style="ATX")
    return {"title": title, "content": markdown, "source_url": url}

async def discover_links(base_url: str, max_pages: int = 50) -> list[str]:
    """Find all internal links (crawl basic pages)"""
    to_visit = [base_url]
    visited, results = set(), []

    while to_visit and len(results) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            html = await fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            results.append(url)

            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if link.startswith(base_url) and link not in visited:
                    to_visit.append(link)
        except Exception:
            continue

    return results
