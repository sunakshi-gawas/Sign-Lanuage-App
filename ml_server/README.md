# ML Server - TensorFlow Model Inference

High-performance TensorFlow model serving for real-time sign language recognition. This server handles neural network inference and returns sign predictions with confidence scores.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup & Installation](#setup--installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Model Details](#model-details)
- [Performance](#performance)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The ML Server is a specialized FastAPI service that:
- Loads pre-trained TensorFlow sign recognition models
- Performs real-time neural network inference
- Returns sign predictions with confidence scores
- Communicates with the backend API server
- Scales features using pre-fitted scalers

### Key Technologies
- **Framework**: FastAPI (lightweight, async)
- **ML Framework**: TensorFlow 2.12+
- **Server**: Uvicorn
- **Data Processing**: NumPy, Scikit-learn
- **Language**: Python 3.9+

## ✨ Features

- 🔥 Real-time inference (< 50ms per request)
- 🎯 High accuracy sign detection (95%+)
- 📊 Confidence scoring
- ⚡ Async request handling
- 🔄 Batch prediction support
- 📈 Performance metrics
- 🔐 Input validation
- 📝 Comprehensive logging
- 🎨 Swagger documentation

## 📁 Directory Structure

```
ml_server/
│
├── 📚 Documentation
│   ├── README.md                # This file
│   ├── MODEL.md                 # Model details & training
│   └── INFERENCE.md             # Inference guide
│
├── 🚀 Server Files
│   ├── main.py                  # FastAPI app & inference logic
│   └── run_server.sh            # Shell startup script
│
├── 🤖 Model Files
│   └── model/
│       ├── sign_model.h5        # Trained Keras model
│       ├── scaler.pkl           # Feature scaler
│       └── label_map.json       # Sign labels mapping
│
└── 🏗️ Virtual Environment
    └── venv_infer/              # Inference environment
```

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- 1GB RAM minimum
- 500MB disk space for models

### Quick Start

Use the root startup script which handles everything:

```bash
cd /path/to/Sign-Language
python3 start_servers.py
```

This automatically:
- Creates virtual environment if needed
- Installs ML server dependencies
- Starts ML server on port 8001
- Monitors server health

### Manual Setup

**1. Create Virtual Environment**
```bash
cd ml_server
python3 -m venv venv_infer
source venv_infer/bin/activate  # On Windows: venv_infer\Scripts\activate
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Verify Model Files**
```bash
ls -lh model/
# Expected:
# sign_model.h5    (~20MB)
# scaler.pkl       (~5KB)
# label_map.json   (~1KB)
```

**4. Run Server**
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001
```

## 🏃 Running the Server

### Development Mode

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

The `--reload` flag enables hot-reload when code changes.

### Production Mode

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4
```

### Multiple Workers

For better performance with multiple requests:

```bash
python3 -m uvicorn main:app \
  --host 0.0.0.0 \
  --port 8001 \
  --workers 4 \
  --loop uvloop  # Optional: faster event loop
```

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Check Server Status

```bash
# Health check
curl http://localhost:8001/health

# View API docs
# Open: http://localhost:8001/docs
```

## 🔌 API Endpoints

### Health Check
```http
GET /health
```

Returns server status and model information.

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_version": "1.0",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

### Sign Prediction
```http
POST /predict
```

Performs sign recognition on input features.

**Request:**
```json
{
  "features": [
    0.1, 0.2, 0.3, 0.4, 0.5,
    0.6, 0.7, 0.8, 0.9, 1.0,
    ...  // 63 total features (normalized)
  ],
  "confidence_threshold": 0.5
}
```

**Response:**
```json
{
  "predicted_sign": "HELLO",
  "confidence": 0.9847,
  "top_3_predictions": [
    {"sign": "HELLO", "confidence": 0.9847},
    {"sign": "YOU", "confidence": 0.0089},
    {"sign": "THANK", "confidence": 0.0045}
  ],
  "inference_time_ms": 23,
  "timestamp": "2025-12-15T10:30:15Z"
}
```

### Batch Prediction
```http
POST /predict-batch
```

Process multiple samples efficiently.

**Request:**
```json
{
  "samples": [
    [0.1, 0.2, 0.3, ...],
    [0.2, 0.3, 0.4, ...],
    [0.3, 0.4, 0.5, ...]
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {"sign": "HELLO", "confidence": 0.98},
    {"sign": "THANK", "confidence": 0.95},
    {"sign": "YES", "confidence": 0.97}
  ],
  "inference_time_ms": 45
}
```

### Model Information
```http
GET /model-info
```

Returns detailed model metadata.

**Response:**
```json
{
  "model_name": "sign_classifier_v1",
  "version": "1.0.0",
  "architecture": "Dense Neural Network",
  "input_shape": [63],
  "output_shape": [11],
  "supported_signs": [
    "BEST", "DISLIKE", "HELLO", "NO", "OK",
    "PEACE", "ROCK", "SORRY", "THANK", "YES", "YOU"
  ],
  "accuracy": 0.9532,
  "training_date": "2025-11-20",
  "framework": "TensorFlow 2.12"
}
```

## 🤖 Model Details

### Architecture

```
Input Layer (63 features)
    ↓
Dense Layer 1 (256 units, ReLU)
    ↓
Dropout (0.3)
    ↓
Dense Layer 2 (128 units, ReLU)
    ↓
Dropout (0.2)
    ↓
Output Layer (11 units, Softmax)
    ↓
Output (Sign Probabilities)
```

### Training Configuration

```python
# Model architecture
model = Sequential([
    Dense(256, activation='relu', input_shape=(63,)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(11, activation='softmax')  # 11 sign classes
])

# Compilation
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Training
model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        EarlyStopping(patience=10),
        ReduceLROnPlateau()
    ]
)
```

### Feature Engineering

**Input**: 21 hand landmarks × 3 coordinates (x, y, z) = 63 features

**Preprocessing**:
1. Extract hand landmarks from video frames
2. Normalize coordinates (0-1 range)
3. Apply feature scaling (StandardScaler)
4. Generate shape-based features

**Sample Features**:
```
Index 0-20:    Landmark X coordinates
Index 21-41:   Landmark Y coordinates
Index 42-62:   Landmark Z coordinates
```

### Model Files

| File | Size | Purpose |
|------|------|---------|
| `sign_model.h5` | ~20MB | Trained Keras model with weights |
| `scaler.pkl` | ~5KB | Feature normalization scaler |
| `label_map.json` | ~1KB | Sign class mappings |

### Label Mapping

```json
{
  "0": "BEST",
  "1": "DISLIKE",
  "2": "HELLO",
  "3": "NO",
  "4": "OK",
  "5": "PEACE",
  "6": "ROCK",
  "7": "SORRY",
  "8": "THANK",
  "9": "YES",
  "10": "YOU"
}
```

## ⚡ Performance

### Inference Speed

**Average Response Times** (tested on MacBook Pro M1):
- Single prediction: 20-30ms
- Batch of 10: 50-70ms
- Batch of 100: 200-250ms

### Memory Usage

- Model loading: 150-200MB
- Per inference: < 5MB
- Batch inference: 10-50MB

### Optimization Techniques

1. **Model Quantization** (future)
   ```python
   converter = tf.lite.TFLiteConverter.from_saved_model(saved_model)
   converter.optimizations = [tf.lite.Optimize.DEFAULT]
   tflite_model = converter.convert()
   ```

2. **Input Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def predict_cached(features_tuple):
       return model.predict(np.array([features_tuple]))
   ```

3. **Async Batch Processing**
   ```python
   async def process_batch(samples):
       return await asyncio.gather(
           *[predict(s) for s in samples]
       )
   ```

## 🛠️ Development

### Project Structure

```python
# main.py
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pickle
import json

app = FastAPI(title="SignVerse ML Server", version="1.0.0")

class PredictRequest(BaseModel):
    features: List[float]
    confidence_threshold: float = 0.5

@app.on_event("startup")
async def load_model():
    global model, scaler, label_map
    model = tf.keras.models.load_model('model/sign_model.h5')
    with open('model/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('model/label_map.json') as f:
        label_map = json.load(f)

@app.post("/predict")
async def predict(request: PredictRequest):
    features = np.array([request.features])
    features = scaler.transform(features)
    predictions = model.predict(features)
    confidence = np.max(predictions[0])
    sign_idx = np.argmax(predictions[0])
    sign_name = label_map[str(sign_idx)]
    return {
        "predicted_sign": sign_name,
        "confidence": float(confidence),
        "inference_time_ms": elapsed_time
    }
```

### Adding New Signs

1. Retrain the model with new data
2. Update `label_map.json`
3. Replace `sign_model.h5`
4. Restart ML server

### Dependencies

```
tensorflow==2.12.0
fastapi==0.100.1
uvicorn==0.24.0
numpy==1.24.3
scikit-learn==1.3.2
pydantic==2.5.0
python-multipart==0.0.6
```

## 🧪 Testing

### Manual Testing

```bash
# Health check
curl http://localhost:8001/health

# Predict
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [0.1, 0.2, 0.3, ...],
    "confidence_threshold": 0.5
  }'

# Model info
curl http://localhost:8001/model-info
```

### Automated Testing

```python
# test_ml_server.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict():
    features = [0.1] * 63  # 63 features
    response = client.post("/predict", json={
        "features": features
    })
    assert response.status_code == 200
    assert "predicted_sign" in response.json()
    assert "confidence" in response.json()
```

Run tests:
```bash
pip install pytest
pytest test_ml_server.py -v
```

## 🔍 Troubleshooting

### Port Already in Use

```bash
# Find process
lsof -i :8001

# Kill process
kill -9 <PID>

# Use different port
python3 -m uvicorn main:app --port 8002
```

### Model File Not Found

```bash
# Verify files exist
ls -lh model/

# Expected output:
# -rw-r--r--  sign_model.h5
# -rw-r--r--  scaler.pkl
# -rw-r--r--  label_map.json
```

### TensorFlow Installation Issues

```bash
# Upgrade pip first
pip install --upgrade pip

# Install TensorFlow
pip install tensorflow==2.12.0

# For M1/M2 Mac
pip install tensorflow-macos tensorflow-metal
```

### Out of Memory (OOM) Errors

```bash
# Reduce batch size
# In your client code, reduce batch_size from 32 to 16

# Or limit workers
python3 -m uvicorn main:app --port 8001 --workers 2
```

### Slow Inference

```bash
# Check CPU usage
top -p $(pgrep -f "uvicorn main:app")

# Use GPU if available
# Ensure TensorFlow is compiled with CUDA support

# Check model optimization
python3 -c "
import tensorflow as tf
model = tf.keras.models.load_model('model/sign_model.h5')
model.summary()
"
```

### Backend Connection Issues

```bash
# Test connectivity
curl http://localhost:8001/health

# Check if backend can reach ML server
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "hello"}'

# If it fails, ensure both servers are running
# Start them: python3 start_servers.py
```

## 📚 Additional Resources

- [TensorFlow Documentation](https://www.tensorflow.org/learn)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)

## 🤝 Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### ML-Specific Guidelines

1. **Always validate input shapes** before prediction
2. **Use appropriate batch sizes** for efficiency
3. **Add error handling** for model inference
4. **Log predictions** for monitoring
5. **Test on sample data** before committing
6. **Document model changes** in MODEL.md

## 📝 License

MIT License - See [../LICENSE](../LICENSE)

---

**Last Updated**: December 15, 2025  
**Version**: 1.0.0  
**ML Framework**: TensorFlow 2.12+
