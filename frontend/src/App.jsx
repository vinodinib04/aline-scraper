import { useState } from "react";

export default function App() {
  const [url, setUrl] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    if (!url) {
      alert("Please enter a website URL");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`https://aline-backend.onrender.com/scrape?site=${encodeURIComponent(url)}`);
      const json = await res.json();
      setData(json);
    } catch (e) {
      alert("Failed to scrape site.");
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 font-sans max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Aline Knowledgebase Scraper</h1>
      
      <input
        type="text"
        placeholder="Enter website URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="border p-2 w-full mb-4"
      />
      
      <button
        onClick={handleScrape}
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Scraping..." : "Scrape"}
      </button>

      {data && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-2">Results for {data.site}</h2>
          {data.items.length === 0 && <p>No pages found or failed to scrape.</p>}
          {data.items.map((item, i) => (
            <div key={i} className="mb-4 border p-2 rounded">
              <h3 className="font-semibold">{item.title}</h3>
              <p><strong>Type:</strong> {item.content_type}</p>
              <a href={item.source_url} target="_blank" className="text-blue-500 underline">Source</a>
              <pre className="bg-gray-100 p-2 mt-2 overflow-x-auto">{item.content}</pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
