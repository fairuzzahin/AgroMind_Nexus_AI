from pathlib import Path
import json
import urllib.request
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CSV = DATA / "Crop_recommendation.csv"
MODEL = DATA / "crop_model.joblib"
URLS = [
 "https://raw.githubusercontent.com/atharvaingle/Crop-Recommendation-Dataset/master/Crop_recommendation.csv",
 "https://raw.githubusercontent.com/atharvaingle/Crop-Recommendation-Dataset/main/Crop_recommendation.csv"
]
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

def get_dataset():
    if CSV.exists():
        return pd.read_csv(CSV)
    DATA.mkdir(parents=True, exist_ok=True)
    for url in URLS:
        try:
            print(f"Trying dataset: {url}")
            urllib.request.urlretrieve(url, CSV)
            return pd.read_csv(CSV)
        except Exception as exc:
            print(f"Download failed: {exc}")
            if CSV.exists(): CSV.unlink()
    raise SystemExit(
      "Dataset download failed. Download Crop_recommendation.csv from "
      "https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset "
      f"and place it at {CSV}"
    )

def main():
    df = get_dataset()
    required = FEATURES + ["label"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"CSV missing columns {missing}; expected {required}")
    df = df[required].dropna()
    X, y = df[FEATURES], df["label"].astype(str)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=300, random_state=42, class_weight=None, n_jobs=-1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    metrics = {
        "dataset_rows": int(len(df)),
        "classes": int(y.nunique()),
        "test_rows": int(len(y_test)),
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "macro_f1": round(float(f1_score(y_test, pred, average="macro")), 4),
        "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, pred, labels=model.classes_).tolist(),
        "class_labels": [str(x) for x in model.classes_],
        "features": FEATURES,
        "dataset_note": "Public benchmark dataset; validation performance does not establish local field performance."
    }
    joblib.dump(model, MODEL)
    (DATA / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Saved model: {MODEL}")
    print(f"Accuracy: {metrics['accuracy']} | Macro-F1: {metrics['macro_f1']}")
    print("Metrics saved to data/metrics.json")
if __name__ == "__main__":
    main()
