import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
from data_utils import load_csvs, add_technical_indicators, prepare_features


def build_dataset(folder):
    dict_dfs = load_csvs(folder)
    big = []
    print("\n📊 Loading datasets...")
    for ticker, df in dict_dfs.items():
        print(f"  - {ticker}: {len(df)} rows")
        df2 = add_technical_indicators(df)
        print(f"    after indicators: {len(df2)} rows")
        df2['Ticker'] = ticker
        big.append(df2)
    combined = pd.concat(big, ignore_index=True)
    print(f"\n✅ Combined dataset: {len(combined)} rows, {combined['Ticker'].nunique()} tickers\n")
    return combined


def train_and_save(folder, model_path='model.joblib'):
    df = build_dataset(folder)
    X, y, df_proc = prepare_features(df)
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    # TimeSeries CV
    tscv = TimeSeriesSplit(n_splits=5)
    scores = []

    print("🔄 Cross-validation:")
    for fold, (train_idx, test_idx) in enumerate(tscv.split(X), 1):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        clf = XGBClassifier(
            n_estimators=500,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            use_label_encoder=False,
            eval_metric="logloss"
        )
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        acc = accuracy_score(y_test, preds)
        scores.append(acc)
        print(f"  Fold {fold}: accuracy={acc:.4f}")

    print(f"\n📈 Average CV accuracy: {np.mean(scores):.4f}")

    # Train final model
    final_clf = XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        use_label_encoder=False,
        eval_metric="logloss"
    )
    final_clf.fit(X, y)

    joblib.dump({'model': final_clf, 'features': X.columns.tolist()}, model_path)
    df_proc.to_csv('processed_combined.csv', index=False)

    print(f"\n💾 Saved model → {model_path}")
    print("💾 Saved dataset → processed_combined.csv\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-folder', default='sample_data')
    parser.add_argument('--model-out', default='model.joblib')
    args = parser.parse_args()

    if not os.path.exists(args.data_folder):
        raise FileNotFoundError(f"❌ Data folder not found: {args.data_folder}")

    train_and_save(args.data_folder, args.model_out)
