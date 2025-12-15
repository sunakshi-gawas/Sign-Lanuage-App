# Project Setup Guide

Complete setup instructions for SignVerse AI development and deployment.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Backend Setup](#backend-setup)
4. [ML Server Setup](#ml-server-setup)
5. [Mobile App Setup](#mobile-app-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **OS**: macOS 10.14+, Linux, or Windows with WSL2
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free space
- **Network**: Internet connection for package installation

### Required Software
```bash
# Check Python version (3.9+ required)
python3 --version

# Check pip is installed
pip3 --version

# For Flutter development
flutter --version

# For Git
git --version
```

**Installation:**

**macOS (with Homebrew):**
```bash
# Install Python
brew install python@3.11

# Install Flutter
brew install flutter

# Install Git
brew install git
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
sudo apt install git
# Flutter: https://flutter.dev/docs/get-started/install/linux
```

**Windows (WSL2):**
```bash
# In WSL2 terminal
sudo apt update
sudo apt install python3 python3-venv python3-pip git
# Flutter: https://flutter.dev/docs/get-started/install/windows
```

## Quick Start

For the fastest setup, use the automated startup script:

```bash
cd /path/to/Sign-Language
python3 start_servers.py
```

This single command:
- ✅ Creates virtual environments (if needed)
- ✅ Installs dependencies
- ✅ Starts Backend API (port 8000)
- ✅ Starts ML Server (port 8001)
- ✅ Monitors both servers
- ✅ Provides status updates

**Output:**
```
============================================================
   SignVerse AI - Backend & ML Server Startup
============================================================

⟳ Starting both servers...
✓ Backend starting on http://localhost:8000
✓ ML Server starting on http://localhost:8001

Checking server health...
✓ Backend Server is running on port 8000
✓ ML Server is running on port 8001

============================================================
Both servers are running!
============================================================

Press Ctrl+C to stop both servers
```

## Backend Setup

For manual setup or troubleshooting:

### 1. Navigate to Backend
```bash
cd Sign-Language/backend
```

### 2. Create Virtual Environment
```bash
python3 -m venv train_venv
source train_venv/bin/activate  # macOS/Linux
# OR
.\train_venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencies include:**
- FastAPI - Web framework
- Uvicorn - ASGI server
- Scikit-learn - Machine learning utilities
- TensorFlow - Model inference
- Requests - HTTP client
- Python-dotenv - Environment variables

### 4. Run Backend Server
```bash
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 5. Test Backend
```bash
# In another terminal
curl http://localhost:8000/api/health
# Response: {"status":"healthy","service":"SignVerse AI"}
```

## ML Server Setup

For manual setup or development:

### 1. Navigate to ML Server
```bash
cd Sign-Language/ml_server
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv_infer
source venv_infer/bin/activate  # macOS/Linux
# OR
.\venv_infer\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Key dependencies:**
- TensorFlow - Deep learning
- Scikit-learn - Feature preprocessing
- FastAPI - Web framework
- NumPy - Numerical computing

**Note:** First TensorFlow installation may take 2-5 minutes.

### 4. Verify Models Exist
```bash
ls -la model/
# Should show: sign_model.h5, label_map.json, scaler.pkl
```

### 5. Run ML Server
```bash
python3 main.py
```

**Expected output:**
```
[INFO] Loading model from .../ml_server/model/sign_model.h5
[INFO] Loading label map from .../ml_server/model/label_map.json
[INFO] Model input dim: 63
[INFO] Classes: {0: 'BEST', 1: 'DISLIKE', ...}
[INFO] Loading scaler from .../ml_server/model/scaler.pkl
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### 6. Test ML Server
```bash
# In another terminal
curl -X POST http://localhost:8001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}'
# Response: {"label":"BEST","index":0,"probs":[...]}
```

## Mobile App Setup

### 1. Navigate to Flutter App
```bash
cd Sign-Language/sign_bridge
```

### 2. Get Dependencies
```bash
flutter pub get
```

### 3. List Available Devices
```bash
flutter devices
```

**Output example:**
```
2 connected devices:

Android SDK built for x86 (emulator) • emulator-5554 • android-x86 • Android 12 (API 32)
macOS (desktop)                       • macos         • darwin-x64  • macOS 13.0
```

### 4. Run on Device/Emulator
```bash
# Run on default device
flutter run

# Run on specific device
flutter run -d emulator-5554

# Run with hot reload for development
flutter run

# Stop: Press 'q' in terminal
```

### 5. Build Release APK (Android)
```bash
flutter build apk --release
# Output: build/app/outputs/flutter-app.apk
```

### 6. Build Release App (macOS)
```bash
flutter build macos --release
# Output: build/macos/Build/Products/Release/sign_bridge.app
```

## Verification

Verify everything is working correctly:

### 1. Check All Servers Running
```bash
# Terminal 1
python3 start_servers.py

# Terminal 2 - Run checks
python3 -c "
import requests
import json

# Check backend
try:
    r = requests.get('http://localhost:8000/api/health')
    print('✓ Backend:', r.json())
except:
    print('✗ Backend: Failed')

# Check ML server
try:
    r = requests.post('http://localhost:8001/api/predict',
        json={'features': [0]*63})
    print('✓ ML Server:', r.json()['label'])
except:
    print('✗ ML Server: Failed')
"
```

### 2. Test Mobile App
```bash
cd sign_bridge
flutter run

# In app:
# 1. Allow camera permissions
# 2. Show hand gesture to camera
# 3. Verify sign detection works
```

### 3. Check Log Files
```bash
# Backend logs
tail -f /tmp/backend.log

# ML Server logs
tail -f /tmp/ml_server.log
```

## Troubleshooting

### Virtual Environment Issues

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Verify venv is activated
which python  # Should show /path/to/venv/bin/python

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

**Problem:** `Address already in use` error

**Solution:**
```bash
# Kill existing processes
pkill -f uvicorn
pkill -f "main.py"

# Or for specific ports
lsof -i :8000,:8001  # See what's using ports
kill -9 <PID>         # Kill the process
```

### Model File Not Found

**Problem:** `Model file not found at .../sign_model.h5`

**Solution:**
```bash
# Check model files exist
ls -la ml_server/model/

# If missing, download/train models
# Contact maintainers for pre-trained models
```

### TensorFlow Installation Issues

**Problem:** TensorFlow installation fails or takes too long

**Solution:**
```bash
# Pre-compile wheels (faster)
pip install --no-cache-dir tensorflow

# Or use specific version
pip install tensorflow==2.12.0

# For M1/M2 Macs
pip install tensorflow-macos
```

### Flutter Device Not Found

**Problem:** `No connected devices`

**Solution:**
```bash
# Start Android emulator first
emulator -avd Pixel_5_API_32 &

# Then list devices
flutter devices

# Or connect physical device
adb devices
```

### Camera Permission Issues (Mobile)

**Problem:** App crashes when accessing camera

**Solution:**
1. Grant camera permissions in system settings
2. Check `AndroidManifest.xml` has camera permission
3. Check `Info.plist` has NSCameraUsageDescription (iOS)
4. Restart app and grant permissions when prompted

## Advanced Configuration

### Change Server Ports

**Backend:**
```python
# backend/app/main.py - Change port
uvicorn.run(app, host="0.0.0.0", port=8080)
```

**ML Server:**
```python
# ml_server/main.py - Change port
uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Enable Debugging

**Python:**
```bash
# Backend
export PYTHONUNBUFFERED=1
python3 -m uvicorn app.main:app --log-level debug

# ML Server
export PYTHONUNBUFFERED=1
python3 main.py
```

**Flutter:**
```bash
flutter run --verbose
```

### Database Setup (Optional)

```bash
# If adding database support
pip install sqlalchemy
python3 -m alembic init alembic
```

## Next Steps

1. ✅ **Setup complete** - Servers running on ports 8000, 8001
2. 📱 **Test mobile app** - Run Flutter app and detect signs
3. 🤖 **Explore ML** - Check model architecture in `train_sign_model.py`
4. 🔧 **Customize** - Add new signs, languages, or features
5. 📤 **Deploy** - Use Docker, AWS, or preferred platform

## Support

For additional help:
1. Check [README.md](README.md)
2. See [CONTRIBUTING.md](CONTRIBUTING.md)
3. Open GitHub Issue with details
4. Contact maintainers

---

**You're all set! Happy developing! 🚀**
