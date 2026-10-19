from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "data" / "crop_model.joblib"
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

def load_model():
    if not MODEL_PATH.exists():
        raise RuntimeError("Model not trained. Run: python scripts/train_model.py")
    return joblib.load(MODEL_PATH)

def predict(model, values: dict):
    row = pd.DataFrame([[values[k] for k in FEATURES]], columns=FEATURES)
    crop = str(model.predict(row)[0])
    probs = model.predict_proba(row)[0]
    classes = list(model.classes_)
    ranked = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]
    importances = sorted(
        [{"feature": f, "importance": float(v)} for f, v in zip(FEATURES, model.feature_importances_)],
        key=lambda x: x["importance"], reverse=True
    )
    return {
        "crop": crop,
        "model_score": round(float(max(probs)), 4),
        "top_alternatives": [{"crop": str(c), "model_score": round(float(p), 4)} for c, p in ranked],
        "feature_importance": importances,
        "explanation": f"The model selected {crop}. Its most influential overall features for this trained model are "
                       + ", ".join(x["feature"] for x in importances[:3]) + ". These are global model importances, not a local causal explanation."
    }
