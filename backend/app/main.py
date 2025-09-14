from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .scraper import scrape_page, discover_links
import asyncio

app = FastAPI(title="Aline Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aline-scraper.vercel.app",  # your frontend domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scrape")
async def scrape_site(url: str, max_pages: int = 50):
    try:
        links = await discover_links(url, max_pages=max_pages)
        tasks = [scrape_page(link) for link in links]
        pages = await asyncio.gather(*tasks, return_exceptions=True)

        items = []
        for p in pages:
            if isinstance(p, Exception): 
                continue
            items.append({
                "title": p["title"],
                "content": p["content"],
                "content_type": "blog",  # heuristic could be smarter
                "source_url": p["source_url"]
            })

        return {"site": url, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
