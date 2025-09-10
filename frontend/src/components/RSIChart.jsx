import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from "recharts";

export default function RSIChart({ data = [] }) {
  const rsiData = (data || []).map(d => ({
    date: d.Date,
    rsi: parseFloat(d.Rsi_14) || 50
  }));

  return (
    <div style={{ width: "100%", height: 200 }}>
      <ResponsiveContainer>
        <LineChart data={rsiData}>
          <XAxis dataKey="date" hide />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <ReferenceLine y={70} stroke="red" strokeDasharray="3 3" />
          <ReferenceLine y={30} stroke="green" strokeDasharray="3 3" />
          <Line type="monotone" dataKey="rsi" stroke="#9333ea" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
