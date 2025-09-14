import React, { useState } from "react"
import { motion } from "framer-motion"

export default function App() {
  const [url, setUrl] = useState("")
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleScrape = async () => {
    setLoading(true)
    setData(null)
    try {
      const API_BASE = import.meta.env.VITE_API_URL
      const res = await fetch(`${API_BASE}/scrape`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      })
      const json = await res.json()
      setData(json)
    } catch (e) {
      alert("Error: " + e.message)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-white to-gray-100">
      <motion.h1
        className="text-4xl font-bold mb-6"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Aline Scraper
      </motion.h1>

      <div className="flex gap-2 mb-6">
        <input
          type="text"
          placeholder="Enter site URL..."
          className="px-4 py-2 border rounded-xl w-96 shadow-sm"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button
          onClick={handleScrape}
          className="bg-black text-white px-6 py-2 rounded-xl shadow hover:bg-gray-800"
          disabled={loading}
        >
          {loading ? "Scraping..." : "Import"}
        </button>
      </div>

      {data && (
        <div className="bg-white shadow-xl rounded-2xl p-6 w-3/4 max-w-3xl overflow-auto h-[400px]">
          <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
