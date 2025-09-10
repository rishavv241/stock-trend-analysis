import React, { useEffect, useState } from "react";
import axios from "axios";
import StockChart from "./StockChart";
import RSIChart from "./RSIChart";
import PredictionPanel from "./PredictionPanel";
import FutureScopePanel from "./FutureScopePanel";   // ✅ new import

export default function Dashboard() {
  const [tickers, setTickers] = useState([]);
  const [selected, setSelected] = useState(null);
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load tickers on mount
  useEffect(() => {
    axios.get("http://localhost:8000/api/tickers")
      .then(r => {
        setTickers(r.data);
        if (r.data && r.data.length > 0) setSelected(r.data[0]);
      })
      .catch(err => console.error(err));
  }, []);

  // Load time series when ticker changes
  useEffect(() => {
    if (!selected) return;
    setLoading(true);
    axios.get(`http://localhost:8000/api/stock/${selected}/timeseries?limit=365`)
      .then(res => {
        setSeries(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [selected]);

  return (
    <div className="dashboard">
      {/* Dropdown selector */}
      <div className="card">
        <h2>Select Stock</h2>
        <select value={selected || ""} onChange={e => setSelected(e.target.value)}>
          {tickers.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>

      {/* Price + anomalies chart */}
      <div className="card">
        <h2>{selected} — Closing Price & Anomalies</h2>
        {loading ? <div>Loading...</div> : <StockChart data={series} />}
      </div>

      {/* RSI chart */}
      <div className="card">
        <h2>{selected} — RSI (14-day)</h2>
        <RSIChart data={series} />
      </div>

      {/* Prediction panel */}
      <div className="card">
        <PredictionPanel series={series} />
      </div>

      {/* 🚀 Future scope panel */}
      <FutureScopePanel />
    </div>
  );
}
