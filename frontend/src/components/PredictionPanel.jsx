import React, { useEffect, useState } from "react";
import axios from "axios";

export default function PredictionPanel({ series }) {
  const [result, setResult] = useState(null);

  useEffect(() => {
    if (!series || series.length === 0) return;
    const latest = series[series.length - 1];
    axios.post("http://localhost:8000/api/predict", { features: latest })
      .then(r => setResult(r.data))
      .catch(err => console.error(err));
  }, [series]);

  if (!result) return <div>Loading prediction...</div>;

  return (
    <div className="prediction card">
      <h2>🤖 Next-Day Prediction</h2>
      <div>
        {result.prediction === 1
          ? <span className="prediction-up">UP 📈</span>
          : <span className="prediction-down">DOWN 📉</span>
        }
      </div>
      <div className="probabilities">
        <p>Probability (Down): {result.probabilities[0].toFixed(3)}</p>
        <p>Probability (Up): {result.probabilities[1].toFixed(3)}</p>
      </div>
    </div>
  );
}
