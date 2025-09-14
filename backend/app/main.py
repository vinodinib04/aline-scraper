
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup
import markdownify as md
from urllib.parse import urljoin, urlparse
import re

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aline-scraper.vercel.app"],  # replace with frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a['href']
        if not href.startswith("http"):
            href = urljoin(base_url, href)
        # Only same domain
        if urlparse(href).netloc == urlparse(base_url).netloc:
            links.add(href)
    return links

def scrape_page(url):
    try:
        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Grab main content heuristically
        main_content = soup.find('main') or soup.find('article') or soup
        text_md = md(str(main_content))
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else url
        return {"title": title, "content": text_md, "source_url": url}
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

@app.get("/scrape")
def scrape_site(site: str = Query(..., description="Website URL to scrape")):
    try:
        resp = httpx.get(site, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch site: {e}"}

    links = extract_links(site, resp.text)
    items = []

    for link in links:
        scraped = scrape_page(link)
        if scraped:
            # Guess content_type (simple heuristic)
            if re.search(r'blog|article|post', link, re.I):
                content_type = "blog"
            elif re.search(r'podcast', link, re.I):
                content_type = "podcast_transcript"
            elif re.search(r'interview', link, re.I):
                content_type = "call_transcript"
            else:
                content_type = "other"
            scraped["content_type"] = content_type
            items.append(scraped)

    return {"site": site, "items": items}





