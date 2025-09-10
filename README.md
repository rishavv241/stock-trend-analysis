# 📊 Stock Trend Analysis using AI/ML  
**Submitted by:** Rishav Kumar (IIT Ropar Minor in AI Program)  

---

## 📝 Project Overview  
This project analyses stock market data of major Indian companies and builds an AI/ML-powered dashboard to visualize technical indicators, anomalies, and predict stock trends.  

The system has two parts:  
- **Backend (FastAPI + Python)** → Handles data preprocessing, feature engineering, model training (RandomForest/XGBoost), and serves prediction APIs.  
- **Frontend (React + Vite + Recharts)** → Provides a clean, interactive dashboard with charts, anomalies, RSI, and next-day trend predictions.  

---

## 🚀 Features
- 📈 **Closing Price Chart** with Moving Averages (MA7 & MA21).  
- ⚠️ **Anomaly Detection** → Highlights sudden daily moves >3%.  
- 📉 **RSI (Relative Strength Index)** visualization with overbought/oversold thresholds.  
- 🤖 **Next-Day Prediction** → AI model predicts UP/DOWN with probabilities.  
- 🔮 **Future Scope Panel** → Outlines advanced AI extensions (multi-day forecasting, sentiment analysis, model comparison).  

---

## 📂 Project Structure
stock-trend-analysis/
┣ backend/ # FastAPI backend
┃ ┣ app.py # API endpoints
┃ ┣ train.py # Model training script
┃ ┣ data_utils.py # Data preprocessing utilities
┃ ┣ requirements.txt # Python dependencies
┃ ┣ model.joblib # Trained ML model
┃ ┣ processed_combined.csv # Processed dataset
┃ ┗ sample_data/ # Stock CSV files
┣ frontend/ # React frontend
┃ ┣ src/ # Components (Dashboard, StockChart, RSIChart, etc.)
┃ ┣ index.html
┃ ┣ package.json
┃ ┣ vite.config.js
┃ ┗ styles.css
┣ README.md # Project documentation

yaml


## ⚙️ Setup & Installation

### 1️⃣ Backend Setup (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # (Mac/Linux)
# or .venv\Scripts\activate  # (Windows)

pip install -r requirements.txt

# Train model
python train.py --data-folder sample_data --model-out model.joblib

# Start backend server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
👉 Backend will run at: http://localhost:8000

Test endpoints:

http://localhost:8000/api/tickers

http://localhost:8000/api/stock/RELIANCE/timeseries?limit=365

2️⃣ Frontend Setup (React + Vite)
bash
Copy code
cd frontend
npm install
npm run dev
👉 Frontend will run at: http://localhost:5173



##🖥️ Dashboard Sections
Select Stock → Dropdown of available tickers.

Closing Price & Anomalies → Line chart with anomalies marked in red.

RSI (14-day) → Momentum oscillator chart with overbought/oversold lines.

Next-Day Prediction → AI model output (UP/DOWN + probability).

Future Scope Panel → Planned AI features like multi-day forecasting.

##📊 Dataset
Collected stock price data for RELIANCE, TCS, INFY, HDFCBANK, ITC.

Each file contains ~1200 rows of OHLCV (Open, High, Low, Close, Volume).

Features engineered:

Moving Averages (7, 21, 50, 200)

Daily Returns & Rolling Volatility

RSI (14-day)

Volume change

Target (next-day up/down)


###🤖 AI/ML Features in Detail

##1. Feature Engineering
Moving Averages (MA7, MA21, MA50, MA200) → capture trend direction.

RSI (Relative Strength Index) → momentum indicator to detect overbought/oversold conditions.

Volatility (21-day rolling std) → quantifies market uncertainty.

Daily Returns → percentage change in stock price.

Volume Change → highlights unusual trading activity.

Anomaly Detection → identifies abnormal daily changes (>3%).

##2. AI Models
RandomForest Classifier (baseline model).

XGBoost Classifier (final model) → more robust with tabular time-series features.

Training Strategy:

Input = engineered technical indicators.

Output = binary target (1 = price goes UP next day, 0 = price goes DOWN).

5-Fold Cross Validation → ensures model generalization.

Performance: ~51% accuracy (slightly above random baseline).

Shows potential but also reflects the inherent difficulty of short-term stock prediction.

##3. AI Integration with Dashboard
Backend serves predictions through FastAPI → /api/predict.

Frontend consumes model output → displays:

UP/DOWN prediction

Probabilities for each class

Visual AI Features:

Prediction panel

RSI chart (model input)

Anomalies marked in chart

##4. Future AI Enhancements (Planned)
Multi-Day Forecasting → LSTM/GRU for sequential price prediction.

Sentiment Analysis → integrate financial news/social media signals.

Model Comparison → allow switching between RandomForest, XGBoost, and Deep Learning models.

📹 Demo Video & Report
All presentation materials (Report, Slides, Demo Video) are available inside the
📂 Presentation & Report subfolder on Google Drive.

##👨‍💻 Author
##Rishav Kumar
##Minor in AI, IIT Ropar