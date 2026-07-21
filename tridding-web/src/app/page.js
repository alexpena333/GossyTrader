"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [dashboard, setDashboard] = useState(null);
  const [trending, setTrending] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const [selectedAsset, setSelectedAsset] = useState(null);
  const [tradeAmount, setTradeAmount] = useState("");
  const [tradeMessage, setTradeMessage] = useState("");

  useEffect(() => {
    async function fetchBackendData() {
      try {
        const dashRes = await fetch("http://localhost:8000/api/v1/portfolio/user_123/dashboard");
        const dashData = await dashRes.json();
        setDashboard(dashData);

        const trendRes = await fetch("http://localhost:8000/api/v1/market/trending");
        const trendData = await trendRes.json();
        setTrending(trendData);

        const newsRes = await fetch("http://localhost:8000/api/v1/market/news");
        const newsData = await newsRes.json();
        setNews(newsData);

        setLoading(false);
      } catch (error) {
        console.error("Error connecting to Python backend:", error);
        setLoading(false);
      }
    }
    fetchBackendData();
  }, []);

  const handleSearch = async (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    if (!query) {
      setSearchResults([]);
      return;
    }
    try {
      const res = await fetch(`http://localhost:8000/api/v1/market/search?q=${query}`);
      const data = await res.json();
      setSearchResults(data);
    } catch (err) {
      console.error("Search error:", err);
    }
  };

  const handlePlaceFuture33 = async (e) => {
    e.preventDefault();
    if (!selectedAsset) return;
    try {
      const res = await fetch("http://localhost:8000/api/v1/future33/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_123",
          asset_symbol: selectedAsset.symbol,
          amount: parseFloat(tradeAmount),
          target_price: selectedAsset.current_price * 1.1,
          expiration_date: new Date(Date.now() + 86400000 * 7).toISOString()
        })
      });
      const data = await res.json();
      if (res.ok) {
        setTradeMessage(data.message);
        setTradeAmount("");
        const dashRes = await fetch("http://localhost:8000/api/v1/portfolio/user_123/dashboard");
        setDashboard(await dashRes.json());
      } else {
        setTradeMessage(`Error: ${data.detail}`);
      }
    } catch (err) {
      setTradeMessage("Failed to connect to backend engine.");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center font-mono">
        LOADING TRIDDING ENGINE...
      </div>
    );
  }

  const isGreen = dashboard?.is_positive;

  return (
    <main className="min-h-screen bg-black text-white p-6 md:p-12 font-sans selection:bg-green-500 selection:text-black">
      <div className="max-w-5xl mx-auto space-y-8">
        <header className="flex justify-between items-center border-b border-zinc-800 pb-6">
          <div>
            <h1 className="text-2xl font-black tracking-tighter text-zinc-100">TRIDDING.</h1>
            <p className="text-xs text-zinc-500 font-mono">INSTITUTIONAL GRADE ENGINE</p>
          </div>
          <div className="text-right">
            <span className="text-xs bg-zinc-900 border border-zinc-800 px-3 py-1 rounded-full font-mono text-zinc-400">
              USER: user_123
            </span>
          </div>
        </header>

        {/* Dashboard Portfolio Card & Performance Chart */}
        <div className="bg-zinc-950 border border-zinc-900 rounded-3xl p-8 shadow-2xl space-y-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <p className="text-sm font-mono text-zinc-500 uppercase tracking-wider">Portfolio Net Worth</p>
              <h2 className="text-5xl font-extrabold tracking-tight mt-1 text-zinc-100">
                ${dashboard?.total_balance?.toLocaleString("en-US", { minimumFractionDigits: 2 }) || "0.00"}
              </h2>
              <div className={`flex items-center gap-2 mt-3 font-semibold text-sm ${isGreen ? "text-green-500" : "text-red-500"}`}>
                <span className="text-lg">{isGreen ? "▲" : "▼"}</span>
                <span>
                  {isGreen ? "+" : ""}${dashboard?.total_profit_loss} ({dashboard?.profit_loss_percentage}%)
                </span>
                <span className="text-zinc-500 font-normal ml-2">All time vs S&P 500</span>
              </div>
            </div>
            <div className="flex gap-4 font-mono text-xs bg-zinc-900/80 border border-zinc-800 p-4 rounded-2xl">
              <div>
                <p className="text-zinc-500">Free Cash</p>
                <p className="text-white text-base font-bold mt-1">${dashboard?.available_buying_power}</p>
              </div>
              <div className="border-l border-zinc-800 pl-4">
                <p className="text-zinc-500">In Escrow</p>
                <p className="text-green-400 text-base font-bold mt-1">${dashboard?.invested_capital}</p>
              </div>
            </div>
          </div>

          {/* Gráfica Comparativa SVG vs S&P 500 */}
          <div className="pt-6 border-t border-zinc-900 space-y-3">
            <div className="flex justify-between items-center text-xs font-mono text-zinc-400">
              <span>Performance Chart (30 Days)</span>
              <div className="flex items-center gap-4">
                <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-green-500 inline-block"></span> Tridding Portfolio</span>
                <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-zinc-500 inline-block"></span> S&P 500 Benchmark</span>
              </div>
            </div>
            <div className="h-44 w-full bg-black/40 border border-zinc-900 rounded-2xl p-4 relative flex items-end">
              <svg className="absolute inset-0 w-full h-full p-4 overflow-visible" viewBox="0 0 500 150" preserveAspectRatio="none">
                {/* S&P 500 Benchmark Line (Gray) */}
                <path d="M 0,100 Q 125,80 250,90 T 500,60" fill="none" stroke="#71717a" strokeWidth="2" strokeDasharray="4 4" opacity="0.6" />
                {/* Tridding Portfolio Line (Dynamic Green/Red) */}
                <path d="M 0,120 Q 125,100 250,70 T 500,25" fill="none" stroke={isGreen ? "#22c55e" : "#ef4444"} strokeWidth="3" />
              </svg>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-bold text-zinc-200">Explore Market</h3>
          <input
            type="text"
            placeholder="Search any ticker or company name (e.g. AMZN, GOOGL, TSLA)..."
            value={searchQuery}
            onChange={handleSearch}
            className="w-full bg-zinc-950 border border-zinc-800 rounded-2xl px-5 py-4 text-white placeholder-zinc-600 focus:outline-none focus:border-zinc-500 transition-colors"
          />
          {searchResults.length > 0 && (
            <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-4 space-y-2">
              {searchResults.map((asset) => (
                <div key={asset.symbol} className="flex justify-between items-center p-3 hover:bg-zinc-900 rounded-xl transition-colors cursor-pointer" onClick={() => setSelectedAsset(asset)}>
                  <div>
                    <span className="font-bold text-white">{asset.symbol}</span>
                    <span className="text-zinc-500 text-sm ml-2">{asset.name}</span>
                  </div>
                  <div className="text-right">
                    <div className="font-mono">${asset.current_price}</div>
                    <div className={`text-xs ${asset.change_24h_percent >= 0 ? "text-green-500" : "text-red-500"}`}>
                      {asset.change_24h_percent >= 0 ? "+" : ""}{asset.change_24h_percent}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-bold text-zinc-200">Top Movers</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {trending.map((asset) => {
              const isAssetPositive = asset.change_24h_percent >= 0;
              return (
                <div 
                  key={asset.symbol} 
                  onClick={() => setSelectedAsset(asset)}
                  className="bg-zinc-950 border border-zinc-900 p-5 rounded-2xl hover:border-zinc-700 transition-all cursor-pointer flex flex-col justify-between"
                >
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-lg text-white">{asset.symbol}</span>
                      <span className={`text-xs px-2 py-1 rounded-md font-mono ${isAssetPositive ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500"}`}>
                        {isAssetPositive ? "+" : ""}{asset.change_24h_percent}%
                      </span>
                    </div>
                    <p className="text-xs text-zinc-500 mt-1">{asset.name}</p>
                  </div>
                  <div className="mt-6 flex justify-between items-end">
                    <span className="text-xl font-mono font-bold">${asset.current_price}</span>
                    <button className="text-xs bg-white text-black font-bold px-3 py-1.5 rounded-lg hover:bg-zinc-200 transition-colors">
                      Trade F33
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {selectedAsset && (
          <div className="bg-zinc-950 border border-zinc-800 p-6 rounded-3xl space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-bold">Place Future33 Order: <span className="text-green-500">{selectedAsset.symbol}</span></h3>
              <button onClick={() => setSelectedAsset(null)} className="text-zinc-500 hover:text-white">✕</button>
            </div>
            <p className="text-sm text-zinc-400">Current Price: ${selectedAsset.current_price}. Funds will be held in secure escrow.</p>
            
            <form onSubmit={handlePlaceFuture33} className="space-y-4">
              <input 
                type="number" 
                placeholder="Amount to risk ($)" 
                value={tradeAmount}
                onChange={(e) => setTradeAmount(e.target.value)}
                className="w-full bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-white focus:outline-none"
                required
              />
              <button type="submit" className="w-full bg-green-500 hover:bg-green-400 text-black font-bold py-3 rounded-xl transition-colors">
                Confirm Future33 Escrow
              </button>
            </form>
            {tradeMessage && <p className="text-sm font-mono text-zinc-300 mt-2">{tradeMessage}</p>}
          </div>
        )}

        <div className="space-y-4 pt-6 border-t border-zinc-900">
          <h3 className="text-lg font-bold text-zinc-200">Market Intelligence Feed</h3>
          <div className="space-y-3">
            {news.map((item, idx) => (
              <a 
                key={idx} 
                href={item.url} 
                target="_blank" 
                rel="noreferrer"
                className="block bg-zinc-950 border border-zinc-900 p-4 rounded-2xl hover:bg-zinc-900 transition-colors"
              >
                <div className="flex justify-between text-xs font-mono text-zinc-500 mb-1">
                  <span>{item.source}</span>
                  <span>{item.time_posted}</span>
                </div>
                <h4 className="font-semibold text-zinc-200">{item.headline}</h4>
              </a>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
