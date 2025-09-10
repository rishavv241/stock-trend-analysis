import React from "react";

export default function MetricsPanel({ features = {} }) {
  if (!features || Object.keys(features).length === 0)
    return <div>No features loaded</div>;

  return (
    <div>
      <div className="panel-title">📌 Features (Latest)</div>
      {Object.entries(features).map(([num, val]) => (
        <div key={num} className="feature-item">
          {num}. {val}
        </div>
      ))}
    </div>
  );
}
