from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import os
from pydantic import BaseModel

app = FastAPI(title="Stock Trend Analysis API")

# ✅ Proper CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "model.joblib"
DATA_PATH = "processed_combined.csv"

model_bundle = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
df_all = pd.read_csv(DATA_PATH, parse_dates=["Date"]) if os.path.exists(DATA_PATH) else None


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/tickers")
def tickers():
    if df_all is None:
        raise HTTPException(500, "Dataset missing. Train model first.")
    return sorted(df_all["Ticker"].unique().tolist())


@app.get("/api/stock/{ticker}/timeseries")
def stock_timeseries(ticker: str, limit: int = 365):
    """Send chart data (Date, Close, RSI, MA7, MA21)"""
    if df_all is None:
        raise HTTPException(500, "Dataset missing.")
    t = ticker.upper()
    d = df_all[df_all["Ticker"] == t].sort_values("Date").tail(limit).copy()
    if d.empty:
        raise HTTPException(404, f"No data for {t}")
    d["Date"] = d["Date"].astype(str)
    return d[["Date", "Close", "MA_7", "MA_21", "Rsi_14"]].to_dict(orient="records")


class PredictRequest(BaseModel):
    features: dict


@app.post("/api/predict")
def predict(req: PredictRequest):
    if model_bundle is None:
        raise HTTPException(500, "Model not trained.")
    model = model_bundle["model"]
    feats = model_bundle["features"]
    row = [req.features.get(f, 0) for f in feats]
    pred = int(model.predict([row])[0])
    prob = model.predict_proba([row])[0].tolist()
    return {"prediction": pred, "probabilities": prob}
