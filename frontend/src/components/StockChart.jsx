import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Scatter
} from "recharts";

export default function StockChart({ data = [] }) {
  // Build chartData with anomaly points
  const chartData = (data || []).map((d, i, arr) => {
    const prev = i > 0 ? parseFloat(arr[i - 1]?.Close) : null;
    const curr = parseFloat(d.Close);
    let anomalyValue = null;

    if (prev && prev > 0) {
      const change = ((curr - prev) / prev) * 100;
      if (Math.abs(change) > 3) {
        anomalyValue = curr; // mark anomaly point
      }
    }

    return {
      date: d.Date,
      close: curr || 0,
      ma7: parseFloat(d.MA_7) || 0,
      ma21: parseFloat(d.MA_21) || 0,
      anomaly: anomalyValue
    };
  });

  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer>
        <LineChart data={chartData}>
          {/* Axes + tooltip + legend */}
          <XAxis dataKey="date" minTickGap={20} />
          <YAxis />
          <Tooltip />
          <Legend />

          {/* Closing Price line */}
          <Line
            type="monotone"
            dataKey="close"
            name="Close"
            stroke="#2563eb"
            dot={false}
          />

          {/* Moving averages */}
          <Line
            type="monotone"
            dataKey="ma7"
            name="MA 7"
            stroke="#16a34a"
            dot={false}
            strokeDasharray="4 4"
          />
          <Line
            type="monotone"
            dataKey="ma21"
            name="MA 21"
            stroke="#f59e0b"
            dot={false}
          />

          {/* Anomalies as red dots */}
          <Scatter dataKey="anomaly" name="Anomalies" fill="red" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
