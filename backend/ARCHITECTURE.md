# Backend Architecture & Design

Deep technical documentation of the backend server architecture, design patterns, and implementation details.

## 📋 Table of Contents

- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Code Structure](#code-structure)
- [Data Flow](#data-flow)
- [Design Patterns](#design-patterns)
- [Database Schema](#database-schema)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)
- [Security](#security)

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Mobile App (Flutter)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  UI Layer                                            │   │
│  │  - Camera Frame Capture                             │   │
│  │  - Sign Display                                     │   │
│  │  - Text Input                                       │   │
│  └─────────────────────┬────────────────────────────────┘   │
│                        │ HTTP                                │
│                        │ JSON                                │
└────────────────────────┼────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   Backend API Server (FastAPI)     │
        │   Port: 8000                       │
        ├────────────────────────────────────┤
        │  Endpoints:                        │
        │  - /api/health                     │
        │  - /api/translate                  │
        │  - /sign_gifs/{sign_name}          │
        ├────────────────────────────────────┤
        │  Middleware:                       │
        │  - CORS                            │
        │  - Request Validation              │
        │  - Error Handling                  │
        └──────────────┬─────────────────────┘
                       │ HTTP/JSON
                       │
        ┌──────────────▼─────────────────────┐
        │  ML Server (TensorFlow)            │
        │  Port: 8001                        │
        ├────────────────────────────────────┤
        │  Services:                         │
        │  - Sign Classification             │
        │  - Model Inference                 │
        │  - Label Mapping                   │
        └────────────────────────────────────┘
```

### Component Interactions

```
Request Flow:
1. Mobile App sends HTTP request
   ↓
2. Backend validates request (Pydantic)
   ↓
3. Backend calls ML Server
   ↓
4. ML Server returns prediction
   ↓
5. Backend formats response
   ↓
6. Mobile App receives and displays result
```

## 💻 Technology Stack

### Core Framework
- **FastAPI** (0.100+)
  - Modern, fast Python web framework
  - Built on async/await
  - Automatic OpenAPI documentation
  - Type hints with Pydantic validation
  
- **Uvicorn** (0.24+)
  - ASGI server
  - High performance
  - Supports auto-reload for development

### Data Validation & Serialization
- **Pydantic** (2.5+)
  - Runtime data validation
  - Type-safe request/response models
  - Automatic JSON schema generation
  - Custom validators

### ML & Data Processing
- **TensorFlow** (2.12+)
  - Neural network models
  - Model loading and inference
  - Saved model formats

- **NumPy** (1.24+)
  - Numerical operations
  - Array manipulations
  - Mathematical functions

- **Pillow** (10.1+)
  - Image processing
  - GIF handling
  - Image transformations

### Web & Networking
- **Requests** (2.31+)
  - HTTP client for ML server communication
  - Connection pooling
  - Error handling

- **Python-multipart** (0.0.6+)
  - File upload handling
  - Form data parsing

### Utilities
- **aiofiles** (23.2+)
  - Async file operations
  - Non-blocking I/O

- **python-dotenv** (optional)
  - Environment configuration

## 📁 Code Structure

### Directory Layout

```
backend/
├── app/
│   ├── __init__.py              # Package marker
│   ├── main.py                  # FastAPI app & routes (200 lines)
│   ├── schemas.py               # Pydantic models (80 lines)
│   └── services/
│       ├── __init__.py
│       ├── sign_classifier.py   # ML integration (150 lines)
│       ├── text_to_sign.py      # Text processing (100 lines)
│       ├── sign_model.h5        # Trained model
│       ├── sign_model.tflite    # Mobile model
│       └── label_map.json       # Sign labels
│
├── main.py                      # Entry point (redirects to app)
├── requirements.txt             # Dependencies
├── train_sign_model.py          # Model training script
├── collect_dataset.py           # Data collection
├── inspect_data.py              # Data inspection
└── plot_training_history.py     # Visualization
```

### File Descriptions

#### `app/main.py` (~200 lines)

Initializes FastAPI application and defines routes:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import TranslateRequest, TranslateResponse
from app.services.sign_classifier import SignClassifier

app = FastAPI(
    title="SignVerse API",
    description="Sign Language Recognition API",
    version="1.0.0"
)

# Initialize services
classifier = SignClassifier()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.post("/api/translate")
async def translate(request: TranslateRequest) -> TranslateResponse:
    # Implementation
    pass

@app.get("/sign_gifs/{sign_name}")
async def get_sign_gif(sign_name: str):
    # Implementation
    pass
```

#### `app/schemas.py` (~80 lines)

Defines Pydantic models for validation:

```python
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=200)
    language: str = Field(default="en")

class TranslateResponse(BaseModel):
    original_text: str
    signs: List[str]
    confidence: float
    timestamp: datetime
    processing_time_ms: int

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
```

#### `app/services/sign_classifier.py` (~150 lines)

Handles ML model loading and inference:

```python
import tensorflow as tf
import json
import requests
from typing import List, Tuple

class SignClassifier:
    def __init__(self):
        self.ml_server_url = "http://localhost:8001"
        self.label_map = self._load_label_map()
    
    def _load_label_map(self) -> dict:
        with open("app/services/label_map.json") as f:
            return json.load(f)
    
    async def classify(self, text: str) -> Tuple[List[str], float]:
        """Call ML server for classification"""
        response = requests.post(
            f"{self.ml_server_url}/predict",
            json={"text": text}
        )
        return response.json()["signs"], response.json()["confidence"]
```

#### `app/services/text_to_sign.py` (~100 lines)

Handles text processing and sign mapping:

```python
from typing import List
import json

class TextToSignConverter:
    def __init__(self):
        self.word_to_sign = self._load_mapping()
    
    def _load_mapping(self) -> dict:
        with open("app/services/label_map.json") as f:
            return json.load(f)
    
    def convert(self, text: str) -> List[str]:
        """Convert text to sign sequence"""
        words = text.lower().split()
        signs = []
        for word in words:
            if word in self.word_to_sign:
                signs.append(self.word_to_sign[word])
        return signs
```

## 🔄 Data Flow

### Text Translation Flow

```
User Input (Text)
      │
      ▼
┌──────────────────────────┐
│  Request Validation      │
│  - Check length          │
│  - Check format          │
│  - Validate language     │
└──────────┬───────────────┘
           │
      ▼ (Valid)
┌──────────────────────────────┐
│  Backend Processing          │
│  - Extract text              │
│  - Prepare payload           │
│  - Add timestamp             │
└──────────┬────────────────────┘
           │
      ▼
┌──────────────────────────────┐
│  ML Server Request           │
│  - Send to port 8001         │
│  - Wait for response         │
│  - Handle timeout            │
└──────────┬────────────────────┘
           │
      ▼
┌──────────────────────────────┐
│  ML Prediction               │
│  - Load model                │
│  - Run inference             │
│  - Get confidence score      │
└──────────┬────────────────────┘
           │
      ▼
┌──────────────────────────────┐
│  Response Formatting         │
│  - Map to sign names         │
│  - Calculate timing          │
│  - Format JSON               │
└──────────┬────────────────────┘
           │
      ▼
Result (JSON Response)
      │
      ▼
Mobile App Display
```

### GIF Retrieval Flow

```
Request: GET /sign_gifs/{sign_name}
      │
      ▼
┌─────────────────────────┐
│  Validate Sign Name     │
│  - Check in label_map   │
│  - Return 404 if invalid│
└────────┬────────────────┘
         │
    ▼ (Valid)
┌─────────────────────────┐
│  Load GIF File          │
│  - Path: sign_gifs/     │
│  - Filename: {name}.gif │
└────────┬────────────────┘
         │
    ▼
┌─────────────────────────┐
│  Stream Response        │
│  - Set content-type     │
│  - Set cache headers    │
│  - Send binary data     │
└────────┬────────────────┘
         │
    ▼
Browser/App Displays GIF
```

## 🎨 Design Patterns

### 1. Dependency Injection

Services are initialized once and reused:

```python
classifier = SignClassifier()

@app.post("/api/translate")
async def translate(request: TranslateRequest):
    # Use shared classifier instance
    result = await classifier.classify(request.text)
    return result
```

### 2. Repository Pattern (Future)

```python
class SignRepository:
    def get_by_name(self, name: str):
        """Get sign metadata by name"""
        pass
    
    def get_all_signs(self):
        """Get all available signs"""
        pass

@app.get("/signs")
async def list_signs(repo: SignRepository = Depends()):
    return repo.get_all_signs()
```

### 3. Service Layer Pattern

```python
# services/sign_service.py
class SignService:
    def __init__(self, classifier: SignClassifier):
        self.classifier = classifier
    
    async def get_signs_for_text(self, text: str):
        return await self.classifier.classify(text)

# Use in route
@app.post("/api/translate")
async def translate(
    request: TranslateRequest,
    service: SignService = Depends()
):
    return await service.get_signs_for_text(request.text)
```

### 4. Factory Pattern

```python
class ModelFactory:
    @staticmethod
    def create_classifier(model_type: str):
        if model_type == "h5":
            return KerasClassifier()
        elif model_type == "tflite":
            return TFLiteClassifier()
```

## 💾 Database Schema (Future)

When adding database support:

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP
);

-- Translation history
CREATE TABLE translations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    input_text VARCHAR(200),
    output_signs JSON,
    confidence FLOAT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Sign metadata
CREATE TABLE signs (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    gif_path VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP
);

-- Analytics
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY,
    endpoint VARCHAR(100),
    method VARCHAR(10),
    response_time INTEGER,
    status_code INTEGER,
    created_at TIMESTAMP
);
```

## ⚠️ Error Handling

### HTTP Status Codes

```python
# 200 - OK
@app.post("/api/translate")
async def translate(request: TranslateRequest):
    return {"status": "ok"}  # 200 OK

# 400 - Bad Request
@app.post("/api/translate")
async def translate(request: TranslateRequest):
    if len(request.text) == 0:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )

# 404 - Not Found
@app.get("/sign_gifs/{sign_name}")
async def get_gif(sign_name: str):
    if not os.path.exists(f"sign_gifs/{sign_name}.gif"):
        raise HTTPException(
            status_code=404,
            detail="Sign not found"
        )

# 500 - Internal Server Error
@app.post("/api/translate")
async def translate(request: TranslateRequest):
    try:
        result = await classify(request.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

### Custom Exception Handlers

```python
class SignClassificationError(Exception):
    pass

@app.exception_handler(SignClassificationError)
async def sign_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@app.post("/api/translate")
async def translate(request: TranslateRequest):
    try:
        result = await classifier.classify(request.text)
    except Exception as e:
        raise SignClassificationError(f"Classification failed: {e}")
```

## ⚡ Performance Optimization

### 1. Connection Pooling

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

# Use session for requests
response = session.post(f"{ml_server_url}/predict", json=data)
```

### 2. Response Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_cached_signs(text: str):
    return await classifier.classify(text)

@app.post("/api/translate")
async def translate(request: TranslateRequest):
    return await get_cached_signs(request.text)
```

### 3. Async Operations

```python
import asyncio

async def classify_multiple(texts: List[str]):
    tasks = [classifier.classify(text) for text in texts]
    results = await asyncio.gather(*tasks)
    return results

@app.post("/api/translate-batch")
async def translate_batch(texts: List[str]):
    return await classify_multiple(texts)
```

### 4. Model Optimization

```python
# Use TFLite for faster inference
import tensorflow as tf

class OptimizedClassifier:
    def __init__(self):
        # Load TFLite model instead of Keras
        self.interpreter = tf.lite.Interpreter(
            model_path="app/services/sign_model.tflite"
        )
        self.interpreter.allocate_tensors()
    
    def classify(self, input_data):
        # Faster inference
        return self.interpreter.get_tensor(...)
```

## 🔐 Security

### Input Validation

```python
from pydantic import BaseModel, Field, validator

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=200)
    
    @validator('text')
    def sanitize_text(cls, v):
        # Remove special characters
        import re
        return re.sub(r'[^a-zA-Z0-9\s]', '', v)
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://10.0.2.2:8000"  # Android emulator
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Restrict methods
    allow_headers=["Content-Type"],  # Restrict headers
)
```

### Rate Limiting (Future)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/translate")
@limiter.limit("100/minute")
async def translate(request: TranslateRequest):
    pass
```

### API Key Authentication (Future)

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.post("/api/translate")
async def translate(
    request: TranslateRequest,
    api_key: str = Depends(verify_api_key)
):
    pass
```

---

**Last Updated**: December 15, 2025  
**Version**: 1.0.0
