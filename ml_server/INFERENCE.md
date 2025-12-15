# Inference Guide

Complete guide to understanding and performing inference with the sign recognition model.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Inference Pipeline](#inference-pipeline)
- [Feature Input](#feature-input)
- [Request/Response Format](#requestresponse-format)
- [Batch Processing](#batch-processing)
- [Error Handling](#error-handling)
- [Performance Tips](#performance-tips)
- [Debugging](#debugging)

## 🚀 Quick Start

### Basic Inference (cURL)

```bash
# Health check
curl http://localhost:8001/health

# Single prediction
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3],
    "confidence_threshold": 0.5
  }'
```

### Python Inference

```python
import requests
import numpy as np

# 63 features from MediaPipe landmarks
features = np.random.rand(63)

response = requests.post(
    'http://localhost:8001/predict',
    json={
        'features': features.tolist(),
        'confidence_threshold': 0.5
    }
)

result = response.json()
print(f"Sign: {result['predicted_sign']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### JavaScript Inference

```javascript
const features = Array(63).fill(0.5);  // 63 features

const response = await fetch('http://localhost:8001/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ features, confidence_threshold: 0.5 })
});

const result = await response.json();
console.log(`Sign: ${result.predicted_sign}`);
console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
```

## 🔄 Inference Pipeline

### Step-by-Step Process

```
1. Capture Video Frame
   ↓
2. Extract Hand Landmarks (MediaPipe)
   └─ 21 landmarks × 3 coordinates = 63 features
   ↓
3. Preprocess Features
   └─ Normalize to [0, 1]
   ↓
4. Apply Feature Scaling
   └─ Use StandardScaler (fitted from training)
   ↓
5. Send to ML Server
   └─ HTTP POST /predict
   ↓
6. Model Inference
   └─ Forward pass through neural network
   ↓
7. Get Predictions
   └─ 11 probability scores (one per sign class)
   ↓
8. Post-Processing
   └─ Apply confidence threshold
   └─ Get top predictions
   ↓
9. Return Result
   └─ Sign name + confidence score
   ↓
10. Display in UI
```

### Timeline Example

```
Timestamp: 0ms   - Frame captured from camera
Timestamp: 2ms   - Hand landmarks extracted
Timestamp: 5ms   - Features normalized
Timestamp: 8ms   - Sent to ML server
Timestamp: 31ms  - Model inference complete
Timestamp: 32ms  - Result received by backend
Timestamp: 34ms  - Response sent to mobile app
                   (Total latency: ~34ms)
```

## 📊 Feature Input

### Feature Array Structure

The model expects exactly 63 input features in this order:

```
Index  | 0-20  | 21-41 | 42-62
-------|-------|-------|-------
Data   | X     | Y     | Z
Coords | Coords| Coords| Coords
```

### Feature Mapping from MediaPipe

```python
import mediapipe as mp

def extract_features_from_landmarks(hand_landmarks):
    """
    Extract 63 features from MediaPipe hand landmarks
    
    Args:
        hand_landmarks: mediapipe hand landmark object
        
    Returns:
        numpy array of 63 features
    """
    features = []
    
    # Extract x, y, z for each of 21 landmarks
    for landmark in hand_landmarks.landmark:
        features.extend([landmark.x, landmark.y, landmark.z])
    
    return np.array(features)
```

### Normalization

```python
from sklearn.preprocessing import StandardScaler
import pickle

# Load pre-fitted scaler (trained on training data)
with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Apply scaling
def normalize_features(raw_features):
    """
    Normalize raw features using training data scaler
    """
    # Reshape for sklearn
    features_2d = raw_features.reshape(1, -1)
    
    # Apply scaler
    normalized = scaler.transform(features_2d)
    
    return normalized.flatten()
```

### Feature Validation

```python
def validate_features(features):
    """
    Validate feature array before sending to model
    """
    # Check length
    if len(features) != 63:
        raise ValueError(f"Expected 63 features, got {len(features)}")
    
    # Check data type
    features = np.array(features, dtype=np.float32)
    
    # Check for NaN/Inf
    if np.any(np.isnan(features)) or np.any(np.isinf(features)):
        raise ValueError("Features contain NaN or Inf values")
    
    # Check value range (after normalization, typically -3 to 3)
    if np.any(np.abs(features) > 5):
        print("Warning: Feature values are unusually large")
    
    return features
```

## 📝 Request/Response Format

### Request Format

```json
{
  "features": [0.1, 0.2, 0.3, ...],
  "confidence_threshold": 0.5
}
```

**Field Details:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `features` | array | Yes | - | 63 float values |
| `confidence_threshold` | float | No | 0.5 | Min confidence to return result |

### Response Format (Success)

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
  "timestamp": "2025-12-15T10:30:15.456789Z"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `predicted_sign` | string | Best matching sign |
| `confidence` | float | Confidence score (0-1) |
| `top_3_predictions` | array | Top 3 predictions with scores |
| `inference_time_ms` | integer | Time taken for inference |
| `timestamp` | string | ISO 8601 timestamp |

### Response Format (Error)

```json
{
  "detail": "Invalid feature array length"
}
```

## 🔄 Batch Processing

### Batch Request

```python
import requests

samples = [
    [0.1, 0.2, 0.3, ...],  # Sample 1
    [0.2, 0.3, 0.4, ...],  # Sample 2
    [0.3, 0.4, 0.5, ...]   # Sample 3
]

response = requests.post(
    'http://localhost:8001/predict-batch',
    json={'samples': samples}
)

results = response.json()
for i, result in enumerate(results['predictions']):
    print(f"Sample {i+1}: {result['sign']} ({result['confidence']:.2%})")
```

### Batch Response

```json
{
  "predictions": [
    {"sign": "HELLO", "confidence": 0.98},
    {"sign": "THANK", "confidence": 0.95},
    {"sign": "YES", "confidence": 0.97}
  ],
  "batch_size": 3,
  "inference_time_ms": 45,
  "average_confidence": 0.9667
}
```

### Performance Comparison

```
Single Predictions:
├── 1 sample:  ~23ms
├── 2 samples: ~46ms (sequential)
├── 10 samples: ~230ms (sequential)

Batch Processing:
├── 1 sample:   ~23ms
├── 2 samples:  ~28ms (4x faster per sample)
├── 10 samples: ~50ms (5x faster per sample)
└── 100 samples: ~250ms (10x faster per sample)

Conclusion: Always use batch processing for multiple samples!
```

## ⚠️ Error Handling

### Common Errors

```json
// Error 1: Invalid feature count
{
  "detail": "Invalid feature array length. Expected 63, got 64"
}

// Error 2: Non-numeric feature
{
  "detail": "Feature values must be numeric"
}

// Error 3: NaN/Inf values
{
  "detail": "Features contain NaN or Inf values"
}

// Error 4: Server error
{
  "detail": "Model inference failed"
}

// Error 5: Connection refused
{
  "detail": "ML Server not responding. Ensure port 8001 is running"
}
```

### Error Handling in Code

```python
import requests
from requests.exceptions import ConnectionError, Timeout

def safe_inference(features):
    """
    Perform inference with error handling
    """
    try:
        # Validate input
        if len(features) != 63:
            raise ValueError(f"Expected 63 features, got {len(features)}")
        
        # Send request
        response = requests.post(
            'http://localhost:8001/predict',
            json={'features': features},
            timeout=5  # 5 second timeout
        )
        
        # Check status
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        # Check confidence
        if result['confidence'] < 0.5:
            print(f"Warning: Low confidence ({result['confidence']:.1%})")
        
        return result
        
    except ValueError as e:
        print(f"Validation error: {e}")
        return None
        
    except ConnectionError:
        print("Error: Cannot connect to ML server (port 8001)")
        return None
        
    except Timeout:
        print("Error: ML server request timed out")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## ⚡ Performance Tips

### 1. Use Batch Processing

```python
# ❌ Slow: Sequential requests
for features in feature_list:
    requests.post('http://localhost:8001/predict', json={'features': features})

# ✅ Fast: Batch request
requests.post('http://localhost:8001/predict-batch', json={'samples': feature_list})
```

### 2. Reuse HTTP Session

```python
import requests

# ❌ Slow: New connection each time
def slow_predict(features):
    return requests.post('http://localhost:8001/predict', json={'features': features})

# ✅ Fast: Reuse session
session = requests.Session()
def fast_predict(features):
    return session.post('http://localhost:8001/predict', json={'features': features})
```

### 3. Cache Scaler

```python
# Load scaler once
import pickle
with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Reuse for all predictions
def preprocess(raw_features):
    return scaler.transform([raw_features])[0]
```

### 4. Parallel Inference (if multiple servers)

```python
import asyncio
import aiohttp

async def parallel_predict(feature_list):
    async with aiohttp.ClientSession() as session:
        tasks = [
            session.post(
                'http://localhost:8001/predict',
                json={'features': f}
            )
            for f in feature_list
        ]
        return await asyncio.gather(*tasks)
```

## 🔍 Debugging

### Check Server Status

```bash
# Health check
curl http://localhost:8001/health

# Verbose output
curl -v http://localhost:8001/health
```

### Test with Sample Data

```python
import numpy as np
import requests

# Create sample data
sample_features = np.random.randn(63).tolist()

response = requests.post(
    'http://localhost:8001/predict',
    json={'features': sample_features}
)

print(response.status_code)
print(response.json())
```

### Monitor Performance

```python
import time

def measure_inference_time(features, iterations=10):
    times = []
    for _ in range(iterations):
        start = time.time()
        response = requests.post(
            'http://localhost:8001/predict',
            json={'features': features}
        )
        elapsed = (time.time() - start) * 1000  # Convert to ms
        times.append(elapsed)
    
    print(f"Min: {min(times):.1f}ms")
    print(f"Max: {max(times):.1f}ms")
    print(f"Avg: {np.mean(times):.1f}ms")
    print(f"P95: {np.percentile(times, 95):.1f}ms")
```

### View Logs

```bash
# Check inference logs
tail -f /tmp/ml_server.log

# Or if running with docker
docker logs -f ml_server_container
```

---

**Last Updated**: December 15, 2025  
**Version**: 1.0.0
