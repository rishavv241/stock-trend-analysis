import pandas as pd
import numpy as np
import os, glob

def load_csvs(folder_path):
    """
    Load all CSVs in folder_path and normalize column names.
    Auto-detects a Date column.
    """
    dfs = {}
    for f in glob.glob(os.path.join(folder_path, "*.csv")):
        name = os.path.splitext(os.path.basename(f))[0].upper()
        
        df = pd.read_csv(f)
        df.columns = [c.strip().capitalize() for c in df.columns]

        # detect date column
        possible_date_cols = [c for c in df.columns if c.lower() in ["date", "timestamp", "day"]]
        if not possible_date_cols:
            raise ValueError(f"❌ {f} has no recognizable Date column. Found: {df.columns.tolist()}")
        
        date_col = possible_date_cols[0]
        df.rename(columns={date_col: "Date"}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)

        df.sort_values('Date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        dfs[name] = df
    return dfs


def add_technical_indicators(df):
    """Add indicators: MA, RSI, Volatility, MACD, Bollinger, Lags."""
    df = df.copy()

    # Moving averages
    for w in [7, 21, 50, 200]:
        df[f'MA_{w}'] = df['Close'].rolling(window=w, min_periods=1).mean()

    # Returns
    df['Return'] = df['Close'].pct_change().fillna(0)

    # Rolling volatility
    df['Volatility_21'] = df['Return'].rolling(window=21, min_periods=1).std().fillna(0)

    # RSI (14)
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.rolling(14, min_periods=1).mean()
    roll_down = down.rolling(14, min_periods=1).mean()
    rs = roll_up / (roll_down + 1e-8)
    df['Rsi_14'] = 100 - (100 / (1 + rs))
    df['Rsi_14'] = df['Rsi_14'].fillna(50)

    # MACD
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Bollinger Bands (20-day)
    df['BB_MA20'] = df['Close'].rolling(20).mean()
    df['BB_Upper'] = df['BB_MA20'] + 2 * df['Close'].rolling(20).std()
    df['BB_Lower'] = df['BB_MA20'] - 2 * df['Close'].rolling(20).std()

    # Lagged returns
    for lag in [1, 5, 10]:
        df[f'Lag_{lag}'] = df['Return'].shift(lag)

    # Volume change
    if "Volume" in df.columns:
        df['Vol_change'] = df['Volume'].pct_change().fillna(0)
    else:
        df['Volume'] = 0
        df['Vol_change'] = 0

    # Target (next day direction)
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    df = df.dropna(subset=['Target']).reset_index(drop=True)

    return df


def prepare_features(df):
    """Extract features + target, clean NaNs/infs."""
    feats = [
        'MA_7','MA_21','MA_50','MA_200',
        'Rsi_14','Volatility_21','Return',
        'MACD','Signal',
        'BB_MA20','BB_Upper','BB_Lower',
        'Lag_1','Lag_5','Lag_10',
        'Vol_change','Volume'
    ]
    for f in feats:
        if f not in df.columns:
            df[f] = 0
    X = df[feats].replace([np.inf, -np.inf], np.nan).fillna(0)
    y = df['Target'].astype(int)
    return X, y, df
