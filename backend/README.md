# Backend API Server

FastAPI-based REST API server for the SignVerse AI sign language recognition system. Provides Sign→Text and Text→Sign APIs, serves sign GIF assets, and integrates with the external ML inference server.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup & Installation](#setup--installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Database & Storage](#database--storage)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The backend server is built with **FastAPI** and **Uvicorn**, providing:

- RESTful API for sign language recognition
- Text-to-sign translation via ML server
- GIF/animation retrieval for detected signs
- Health monitoring and metrics
- CORS support for mobile app integration
- Error handling and validation

### Key Technologies

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **Language**: Python 3.11 (recommended)
- **Validation**: Pydantic 2.5.0
- **Hand Tracking**: cvzone + MediaPipe
- **ML Integration**: External ML server (`ml_server`) via HTTP

## ✨ Features

- 🔍 Sign→Text from feature vectors or camera images (via external ML server)
- 🎯 Real-time API responses
- 📚 Text→Sign using GIF library lookup
- 🌐 CORS-enabled for mobile integration
- 📊 Health check endpoints
- ⚡ Async request handling
- 🔐 Input validation
- 📝 Comprehensive error messages
- 🎨 Interactive API documentation (Swagger UI)
- 🧪 Request/response validation

## 📁 Directory Structure

```
backend/
│
├── app/                            # FastAPI Application
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # FastAPI routes & app entry
│   ├── schemas.py                  # Pydantic request/response models
│   └── services/                   # Business logic services
│       ├── __init__.py
│       ├── sign_classifier.py      # Calls external ML server
│       ├── text_to_sign.py         # Text→Sign GIF lookup utilities
│       ├── translator.py           # Simple text translation helper
│       └── label_map.json          # Sign labels mapping (if needed)
│
├── data/                           # Training dataset (hand landmarks)
│   ├── BEST/ ...                   # Sign samples
│   └── ...
│
├── models/                         # Auxiliary model assets
│   └── hand_landmarker.task        # Hand landmark model (MediaPipe)
│
├── logs/                           # Server logs (optional)
│
├── sign_gifs/                      # Animated GIFs for Text→Sign
│   ├── HELLO.gif
│   ├── PLEASE.gif
│   ├── SORRY.gif
│   ├── THANK_YOU.gif
│   └── YES.gif
│
├── training_plots/                 # Model training visualizations
│
├── collect_dataset.py
├── train_sign_model.py
├── inspect_data.py
├── plot_training_history.py
├── requirements.txt                # Python dependencies
├── README.md                       # This file
```

## 🚀 Setup & Installation

### Prerequisites

- Python 3.11
- pip package manager
- Virtual environment tool (venv)
- 500MB disk space for models and data

### Quick Start

The easiest way is to use the root startup script (Windows `cmd.exe`):

```bat
cd d:\Sign-Language-App\Sign-Language-App
py -3.11 start_servers.py
```

This automatically:

- Creates virtual environments if needed
- Installs dependencies
- Starts backend on port 8000
- Starts ML server on port 8001

### Manual Setup

**1. Create Virtual Environment**

```bat
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
```

**2. Install Dependencies**

```bat
pip install -r requirements.txt
```

**3. Run Server**

```bat
py -3.11 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables hot-reload for development.

## 🏃 Running the Server

### Development Mode

```bat
py -3.11 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bat
py -3.11 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Check Server Status

```bat
rem Health check
curl http://localhost:8000/api/health

rem View API docs
rem Open: http://localhost:8000/docs
```

## 🔌 API Endpoints

### Health Check

```http
GET /api/health
```

Returns quick server status.

**Response:**

```json
{
  "status": "healthy",
  "service": "SignVerse AI"
}
```

### Serve Sign GIF

```http
GET /sign_gifs/{file}.gif
```

Returns animated GIF asset for a given token.

**Example:**

```bat
curl http://localhost:8000/sign_gifs/HELLO.gif --output hello.gif
```

### Sign→Text (features)

```http
POST /api/sign-to-text
```

Classify a sign from a 63-dim feature vector (flattened 21 hand landmarks).

**Request (SignToTextRequest):**

```json
{
  "features": [0.1, -0.2, 0.05, ...],
  "language": "en"
}
```

**Response (SignToTextResponse):**

```json
{
  "text": "Hello",
  "confidence": 0.92
}
```

### Sign→Text (camera image)

```http
POST /api/sign-to-text-image?language=en
```

Classify a sign from a camera frame (binary image body, JPEG/PNG). Automatically detects the hand, extracts landmarks, and calls the ML server.

**Response (SignToTextResponse):**

```json
{
  "text": "Hello",
  "confidence": 0.88
}
```

### Text→Sign (GIF lookup)

```http
POST /api/text-to-sign
```

Tokenizes input text and returns available GIF URLs for each token.

**Request (TextToSignRequest):**

```json
{
  "text": "hello please",
  "sign_language": "ISL"
}
```

**Response (TextToSignResponse):**

```json
{
  "sign_tokens": ["HELLO", "PLEASE"],
  "avatar_animation_ids": ["/sign_gifs/HELLO.gif", "/sign_gifs/PLEASE.gif"]
}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend folder:

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false

# ML Server (external inference)
ML_SERVER_URL=http://127.0.0.1:8001/api/predict
CONF_THRESHOLD=0.15

# CORS
CORS_ORIGINS=["http://localhost:3000","http://10.0.2.2:8000"]

# Logging (optional)
LOG_LEVEL=INFO
LOG_FILE=./logs/backend.log
```

### Dependencies (requirements.txt)

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6

# Data & ML
numpy>=1.26.0
opencv-python>=4.8.0
mediapipe==0.10.14
scikit-learn==1.8.0
cvzone==1.6.1

# API & networking
requests>=2.31.0
anyio>=3.7.1

# Optional
gTTS>=2.4.0
```

## 💾 Database & Storage

### Current Setup

The backend uses:

- **External ML**: `ml_server` for predictions (`/api/predict`)
- **Hand assets**: `models/hand_landmarker.task`
- **GIFs**: `sign_gifs/` directory
- **Logs**: `logs/backend.log`

### Scaling Considerations

For production deployment:

1. **Database**: Add PostgreSQL or MongoDB for

   - User history
   - Translation logs
   - Analytics

2. **Object Storage**: Use S3/Cloud Storage for

   - GIF files
   - Model files
   - Training datasets

3. **Caching**: Implement Redis for
   - Translation cache
   - Model predictions
   - Session management

## 🛠️ Development

### Project Structure

```python
# app/main.py - Key endpoints

@app.get("/api/health")
def health_check():
  return {"status": "healthy", "service": "SignVerse AI"}

@app.post("/api/sign-to-text")
def sign_to_text(req: SignToTextRequest):
  label, conf = classifier.predict(req.features)
  text = label_to_text(label)
  if req.language and req.language != "en":
    text = translate_text(text, req.language)
  return SignToTextResponse(text=text, confidence=float(conf))

@app.post("/api/sign-to-text-image")
async def sign_to_text_image(request: Request):
  # decode image bytes, detect hand, extract landmarks, call ML server
  ...

@app.post("/api/text-to-sign")
def text_to_sign(req: TextToSignRequest):
  tokens = text_to_tokens(req.text)
  urls = [token_to_gif_url(t) for t in tokens if token_to_gif_url(t)]
  return TextToSignResponse(sign_tokens=tokens, avatar_animation_ids=urls)
```

### Adding New Endpoints

1. Define request/response models in `schemas.py`:

```python
from pydantic import BaseModel

class SignRequest(BaseModel):
    sign_name: str
    confidence_threshold: float = 0.8
```

2. Create service method in `services/sign_classifier.py`:

```python
async def classify_sign(sign_name: str):
    # Implementation
    pass
```

3. Add route in `app/main.py`:

```python
@app.post("/api/classify")
async def classify(request: SignRequest):
    result = await classify_sign(request.sign_name)
    return result
```

### Code Style

Follow PEP 8:

```bash
# Format code
pip install black
black app/

# Check style
pip install flake8
flake8 app/

# Type checking
pip install mypy
mypy app/
```

## 🧪 Testing

### Manual Testing

Test endpoints with curl:

```bat
rem Health check
curl http://localhost:8000/api/health

rem Sign→Text (features)
curl -X POST http://localhost:8000/api/sign-to-text ^
  -H "Content-Type: application/json" ^
  -d "{\"features\":[0.1,0.2,0.3],\"language\":\"en\"}"

rem Text→Sign (GIF lookup)
curl -X POST http://localhost:8000/api/text-to-sign ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"hello please\"}"

rem Get sign GIF
curl http://localhost:8000/sign_gifs/HELLO.gif -o hello.gif
```

### Automated Testing

Create `test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
  response = client.get("/api/health")
  assert response.status_code == 200
  data = response.json()
  assert data["status"] == "healthy"

def test_text_to_sign():
  response = client.post("/api/text-to-sign", json={
    "text": "hello"
  })
  assert response.status_code == 200
  data = response.json()
  assert "sign_tokens" in data
  assert "avatar_animation_ids" in data
```

Run tests:

```bat
pip install pytest pytest-asyncio
pytest test_api.py -v
```

## 🔍 Troubleshooting

### Port Already in Use (Windows)

```bat
rem Find process using port 8000
netstat -ano | findstr :8000

rem Kill the process
taskkill /PID <PID> /F

rem Or use different port
py -3.11 -m uvicorn app.main:app --port 8001
```

### Module Not Found Errors

```bat
rem Ensure virtual environment is activated
venv\Scripts\activate

rem Reinstall dependencies
pip install -r requirements.txt

rem Check PYTHONPATH (Windows)
set PYTHONPATH=%PYTHONPATH%;d:\Sign-Language-App\Sign-Language-App\backend
```

### ML Server Connection Issues

```bat
rem Check if ML server is running
curl http://localhost:8001/health

rem Test prediction endpoint
curl -X POST http://localhost:8001/api/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"features\":[0.1,0.2,0.3]}"

rem Check backend logs
type .\logs\backend.log
```

### Model File Not Found

```bat
rem Verify GIF assets exist
dir sign_gifs

rem Verify hand asset
dir models\hand_landmarker.task

rem Verify label map (optional)
type app\services\label_map.json
```

### CORS Errors from Mobile App

Update `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Be specific in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ML Server Connection Issues

```bash
# Check if ML server is running
curl http://localhost:8001/health

# Verify network connectivity
ping localhost

# Check backend logs
tail -f /tmp/backend.log
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [TensorFlow Documentation](https://www.tensorflow.org/learn)

## 🤝 Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Backend-Specific Guidelines

1. **Always validate input** with Pydantic models
2. **Add error handling** for ML server communication
3. **Log important events** for debugging
4. **Add docstrings** to all functions
5. **Test new endpoints** before committing
6. **Update this README** when adding features

## 📝 License

MIT License - See [../LICENSE](../LICENSE)

---

**Last Updated**: December 17, 2025  
**Version**: 1.2.0  
**Maintainer**: XXXXXXXXXX
