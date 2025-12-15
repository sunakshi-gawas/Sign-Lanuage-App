# Backend API Server

FastAPI-based REST API server for the SignVerse AI sign language recognition system. Handles sign translation, API routing, and ML model inference requests.

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
- **Framework**: FastAPI 0.100+
- **Server**: Uvicorn
- **Language**: Python 3.9+
- **Validation**: Pydantic
- **ML Integration**: TensorFlow via separate ML server

## ✨ Features

- 🔍 Sign recognition from video frames
- 🎯 Real-time API responses
- 📚 Sign GIF/animation library
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
├── 📚 Documentation
│   ├── README.md                    # This file
│   ├── API.md                       # Detailed API documentation
│   └── ARCHITECTURE.md              # Architecture details
│
├── 🚀 Server Files
│   ├── app/
│   │   ├── __init__.py             # Package initialization
│   │   ├── main.py                 # FastAPI application & routes
│   │   ├── schemas.py              # Pydantic models for validation
│   │   └── services/               # Business logic
│   │       ├── __init__.py
│   │       ├── sign_classifier.py  # Sign classification logic
│   │       ├── text_to_sign.py     # Text translation to sign
│   │       ├── sign_model.h5       # Trained ML model
│   │       ├── sign_model.tflite   # TFLite model for mobile
│   │       └── label_map.json      # Sign labels mapping
│   │
│   └── start_servers.py            # Server startup script (at root)
│
├── 🤖 ML Training
│   ├── train_sign_model.py         # Model training script
│   ├── collect_dataset.py          # Data collection script
│   ├── inspect_data.py             # Data inspection utility
│   ├── plot_training_history.py    # Visualization script
│   └── requirements.txt            # Python dependencies
│
├── 📊 Data
│   ├── data/                       # Training dataset
│   │   ├── BEST/                   # Sample frames
│   │   ├── HELLO/
│   │   ├── NO/
│   │   ├── OK/
│   │   ├── PEACE/
│   │   ├── SORRY/
│   │   ├── THANK/
│   │   ├── YES/
│   │   ├── YOU/
│   │   ├── ROCK/
│   │   └── DISLIKE/
│   │
│   ├── sign_gifs/                  # GIF assets for UI display
│   └── training_plots/             # Training visualizations
│
├── 🔧 Configuration
│   ├── requirements.txt            # Production dependencies
│   ├── .gitignore                  # Git ignore patterns
│   └── run_backend.sh              # Legacy startup script
│
└── 🏗️ Virtual Environments
    └── train_venv/                 # Training environment
    └── venv/                       # Production environment
```

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment tool (venv)
- 500MB disk space for models and data

### Quick Start

The easiest way is to use the root startup script:

```bash
cd /path/to/Sign-Language
python3 start_servers.py
```

This automatically:
- Creates virtual environment if needed
- Installs dependencies
- Starts backend on port 8000
- Starts ML server on port 8001

### Manual Setup

**1. Create Virtual Environment**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Run Server**
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables hot-reload for development.

## 🏃 Running the Server

### Development Mode

```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Check Server Status

```bash
# Health check
curl http://localhost:8000/api/health

# View API docs
# Open: http://localhost:8000/docs
```

## 🔌 API Endpoints

### Health Check
```http
GET /api/health
```
Returns server status and version.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

### Get Sign GIF
```http
GET /sign_gifs/{sign_name}
```
Returns animated GIF for a detected sign.

**Parameters:**
- `sign_name` (string): Sign name (e.g., "HELLO", "THANK", "YES")

**Response:**
- Content-Type: `image/gif`
- Binary GIF data

**Example:**
```bash
curl http://localhost:8000/sign_gifs/HELLO --output hello.gif
```

### Translate Text to Sign
```http
POST /api/translate
```
Converts text to sign language sequence.

**Request:**
```json
{
  "text": "hello",
  "language": "en"
}
```

**Response:**
```json
{
  "original_text": "hello",
  "signs": ["HELLO"],
  "confidence": 0.98,
  "timestamp": "2025-12-15T10:30:00Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "hello", "language": "en"}'
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend folder:

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false

# ML Server
ML_SERVER_URL=http://localhost:8001

# CORS
CORS_ORIGINS=["http://localhost:3000","http://10.0.2.2:8000"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=/tmp/backend.log

# Model
MODEL_PATH=./app/services/sign_model.h5
LABEL_MAP_PATH=./app/services/label_map.json
```

### Dependencies (requirements.txt)

```
fastapi==0.100.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
aiofiles==23.2.1
pillow==10.1.0
numpy==1.24.3
tensorflow==2.12.0
requests==2.31.0
```

## 💾 Database & Storage

### Current Setup
The backend uses file-based storage for:
- **Models**: `app/services/sign_model.h5` (Keras)
- **Labels**: `app/services/label_map.json` (JSON mapping)
- **GIFs**: `sign_gifs/` directory
- **Logs**: `/tmp/backend.log`

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
# app/main.py - Main FastAPI application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SignVerse API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
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

```bash
# Health check
curl http://localhost:8000/api/health

# Test translation
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world", "language": "en"}'

# Get sign GIF
curl http://localhost:8000/sign_gifs/HELLO -o sign.gif
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
    assert response.json()["status"] == "ok"

def test_translate():
    response = client.post("/api/translate", json={
        "text": "hello",
        "language": "en"
    })
    assert response.status_code == 200
    assert "signs" in response.json()
```

Run tests:
```bash
pip install pytest pytest-asyncio
pytest test_api.py -v
```

## 🔍 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
python3 -m uvicorn app.main:app --port 8001
```

### Module Not Found Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

### TensorFlow Issues on M1/M2 Mac

```bash
# Use conda instead
conda create -n signverse python=3.10
conda activate signverse
conda install -c apple tensorflow-deps
pip install tensorflow-macos tensorflow-metal
```

### Model File Not Found

```bash
# Verify model exists
ls -lh app/services/sign_model.h5

# Check file permissions
chmod 644 app/services/sign_model.h5

# Verify label map
cat app/services/label_map.json
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

**Last Updated**: December 15, 2025  
**Version**: 1.0.0  
**Maintainer**: SignVerse AI Team
