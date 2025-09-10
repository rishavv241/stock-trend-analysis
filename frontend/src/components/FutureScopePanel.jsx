import React from "react";

export default function FutureScopePanel() {
  return (
    <div className="card">
      <h2>🚀 Future Scope — AI Enhancements</h2>
      <ul style={{ lineHeight: "1.8" }}>
        <li><strong>Multi-Day Forecasting</strong>: Use LSTM/GRU or Facebook Prophet to predict stock trends for the next 5–7 days.</li>
        <li><strong>Sentiment Analysis</strong>: Integrate news and social media sentiment with price data for improved predictions.</li>
        <li><strong>Model Comparison</strong>: Compare RandomForest, XGBoost, and Deep Learning models in real-time.</li>
      </ul>
    </div>
  );
}
