# ml_server/main.py

from typing import List, Dict

import json
import os
import pickle

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# ---------- Config ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "sign_model.h5")
LABEL_MAP_PATH = os.path.join(BASE_DIR, "model", "label_map.json")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

# ---------- Pydantic schema ----------

class FeaturesRequest(BaseModel):
    features: List[float]  # 63 floats (21 landmarks * 3 coords)


class PredictionResponse(BaseModel):
    label: str
    index: int
    probs: List[float]


# ---------- Load model & label map ----------

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found at {MODEL_PATH}")

if not os.path.exists(LABEL_MAP_PATH):
    raise RuntimeError(f"Label map file not found at {LABEL_MAP_PATH}")

print(f"[INFO] Loading model from {MODEL_PATH}")
model = load_model(MODEL_PATH)

print(f"[INFO] Loading label map from {LABEL_MAP_PATH}")
with open(LABEL_MAP_PATH, "r") as f:
    raw_map = json.load(f)

INDEX_TO_LABEL: Dict[int, str] = {int(k): v for k, v in raw_map.items()}
NUM_CLASSES = len(INDEX_TO_LABEL)
INPUT_DIM = model.input_shape[1]

print("[INFO] Model input dim:", INPUT_DIM)
print("[INFO] Classes:", INDEX_TO_LABEL)

# Load scaler if available, otherwise create a dummy one
if os.path.exists(SCALER_PATH):
    print(f"[INFO] Loading scaler from {SCALER_PATH}")
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    print("[INFO] Scaler loaded successfully")
else:
    print("[WARN] No scaler found. Using default StandardScaler")
    scaler = StandardScaler()
    # Fit on dummy data (mean=0, std=1)
    scaler.fit(np.random.randn(100, INPUT_DIM))

# ---------- FastAPI app ----------

app = FastAPI(title="Sign ML Inference Server")


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Sign ML inference server running",
        "classes": INDEX_TO_LABEL,
    }


@app.post("/api/predict", response_model=PredictionResponse)
async def predict(req: FeaturesRequest):
    features = req.features

    if len(features) != INPUT_DIM:
        raise HTTPException(
            status_code=400,
            detail=f"Expected {INPUT_DIM} features, got {len(features)}",
        )

    try:
        x = np.array(features, dtype=np.float32).reshape(1, -1)
        # Normalize features using the same scaler as training
        x_normalized = scaler.transform(x)
        preds = model.predict(x_normalized, verbose=0)
        probs = preds[0]

        idx = int(np.argmax(probs))
        label = INDEX_TO_LABEL.get(idx, "UNKNOWN")

        return PredictionResponse(
            label=label,
            index=idx,
            probs=probs.tolist(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
