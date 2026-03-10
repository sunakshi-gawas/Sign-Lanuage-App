# SignVerse AI - Real-Time Sign Language Translation

<p align="center">
  <img src="sign_bridge/assets/logo.png" alt="SignVerse AI Logo" width="120"/>
</p>

A mobile app and server infrastructure for real-time sign language detection and translation to text and speech in multiple languages.

## 🎯 Features

- **Real-time Sign Detection**: Uses MediaPipe for hand landmark detection
- **AI-powered Classification**: TensorFlow-based sign classifier with 100% training accuracy
- **Text-to-Sign Translation**: Convert text to animated sign language GIFs
- **Multi-language Support**: English and Marathi translations
- **Text-to-Speech**: Natural audio output with multiple voice options
- **Network Status**: Real-time online/offline connectivity indicator
- **Modern UI**: Purple & orange themed interface matching brand identity
- **Cross-platform**: Android mobile app with Flutter
- **REST API**: Easy integration with FastAPI backend

## 📱 Supported Signs

Currently trained signs (expandable by adding more training data):

- ✅ BEST
- ✅ HELLO
- ✅ NO
- ✅ YES
- ✅ DISLIKE
- ✅ OK
- ✅ PEACE
- ✅ ROCK
- ✅ SORRY

> **Note**: Additional signs can be added by collecting training data and retraining the model.

## 🏗️ Architecture

```
Sign-Language-App/
├── sign_bridge/              # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart         # App entry point
│   │   ├── screens/          # UI screens
│   │   │   ├── home_screen.dart
│   │   │   ├── sign_to_text_screen_v2.dart
│   │   │   └── text_to_sign_screen.dart
│   │   ├── services/         # API clients
│   │   ├── theme/            # App theming (purple/orange)
│   │   └── widgets/          # Reusable components
│   ├── assets/               # Logo and images
│   ├── android/              # Android native code
│   └── ios/                  # iOS native code
│
├── backend/                  # FastAPI Backend (Port 8000)
│   ├── app/
│   │   ├── main.py           # FastAPI app entry
│   │   ├── schemas.py        # Request/response schemas
│   │   └── services/         # Business logic
│   │       ├── sign_classifier.py
│   │       ├── text_to_sign.py
│   │       └── translator.py
│   ├── sign_gifs/            # Animated sign GIFs
│   ├── requirements.txt
│   ├── models/               # Hand landmarking assets (e.g. hand_landmarker.task)
│   └── venv/                 # Python virtual environment (created by scripts)
│
├── ml_server/                # TensorFlow ML Server (Port 8001)
│   ├── main.py               # ML server entry
│   ├── model/                # Trained models & label maps
│   │   ├── sign_model.h5
│   │   ├── label_map.json
│   │   └── scaler.pkl
│   └── venv_infer/           # Python virtual environment
│
└── start_servers.py          # One-command startup script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 (required - Python 3.13 not compatible with TensorFlow)
- pip and venv
- Flutter SDK 3.10+
- Git

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/Sign-Language-App.git
cd Sign-Language-App
```

2. **Start Backend & ML Server (Recommended)**

```bat
py -3.11 start_servers.py
```

The script will:

- Activate virtual environments automatically
- Start Backend API on `http://localhost:8000`
- Start ML Server on `http://localhost:8001`
- Monitor both servers continuously
- Stop gracefully with `Ctrl+C`

### Manual Setup (Alternative)

**Backend Server:**

```bat
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**ML Server:**

```bat
cd ml_server
py -3.11 -m venv venv_infer
venv_infer\Scripts\activate
pip install -r requirements.txt
rem Install TensorFlow runtime if not present
pip install tensorflow==2.18.0
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

**Flutter App:**

```bash
cd sign_bridge
flutter pub get
flutter run
```

> **Important**: When running on a physical device, update the API base URL in the Flutter app to your computer's local IP address (e.g., `http://192.168.x.x:8000`).

## 📱 App Screens

| Screen           | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| **Home**         | Main dashboard with online status, navigation to features           |
| **Sign to Text** | Real-time camera-based sign detection with front/back camera toggle |
| **Text to Sign** | Convert typed text to animated sign language GIFs                   |

<!-- Screenshots -->
<p align="center">
  <img src="app%20ss/ss1.jpg" alt="App Screenshot 1" width="260"/>
  <img src="app%20ss/ss2.jpg" alt="App Screenshot 2" width="260"/>
  <img src="app%20ss/ss3.jpg" alt="App Screenshot 3" width="260"/>
  <img src="app%20ss/ss4.jpg" alt="App Screenshot 4" width="260"/>
</p>

## 📚 API Documentation

### Backend Health Check

```bash
curl http://localhost:8000/api/health
```

Response:

```json
{
  "status": "healthy",
  "service": "SignVerse AI"
}
```

### Sign→Text (features via Backend)

```http
POST http://localhost:8000/api/sign-to-text
Content-Type: application/json

{
  "features": [0.0, 0.1, 0.2, ...],
  "language": "en"
}
```

### Sign→Text (camera image)

```http
POST http://localhost:8000/api/sign-to-text-image?language=en
```

Binary image body (JPEG/PNG). Backend extracts hand landmarks and calls ML server.

### ML Server Prediction (direct)

```http
POST http://localhost:8001/api/predict
Content-Type: application/json

{
  "features": [0.0, 0.1, ...]  // 63 landmarks × 3 = 63 features
}
```

### Text→Sign (GIF lookup)

```http
POST http://localhost:8000/api/text-to-sign
Content-Type: application/json

{
  "text": "hello please"
}
```

### Serve Sign GIF

```http
GET http://localhost:8000/sign_gifs/HELLO.gif
```

## 🎓 Model Training

The sign classifier model was trained on hand landmark data collected from video recordings using:

- **Feature Extraction**: MediaPipe Hand Pose (21 landmarks × 3 coordinates = 63 features)
- **Model**: TensorFlow Sequential Neural Network
- **Preprocessing**: StandardScaler normalization
- **Training Accuracy**: 100%
- **Confidence Threshold**: 70% (below shows "UNKNOWN")

### Adding New Signs

1. **Collect training data:**

```bash
cd backend
python3.11 collect_dataset.py
```

2. **Train the model:**

```bash
python3.11 train_sign_model.py
```

3. **Copy model to ML server:**

```bash
cp model/sign_model.h5 ../ml_server/model/
cp model/label_map.json ../ml_server/model/
cp model/scaler.pkl ../ml_server/model/
```

4. **Restart the ML server**

## 🛠️ Development

### Project Structure

- **Frontend**: Flutter (Dart) - Real-time camera capture, UI
- **Backend**: FastAPI (Python) - REST API, business logic
- **ML**: TensorFlow (Python) - Model inference, predictions
- **Data**: Training datasets in `backend/data/` directory

### Testing Servers

```bat
rem Check backend
curl http://localhost:8000/api/health

rem Check ML server
curl -X POST http://localhost:8001/api/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"features\":[0,0,0,0,0,0,0,0,0,0]}"
```

### Logs

- Backend logs: `./logs/backend.log`
- ML Server logs: `./ml_server/logs/ml_server.log` (if configured)

## 🔧 Configuration

### Languages (Backend)

Edit `backend/app/main.py` to add/remove language support:

- English (en-US)
- Marathi (mr-IN)

### Model Paths

Models are stored in `ml_server/model/`:

- `sign_model.h5` - TensorFlow model
- `label_map.json` - Sign class labels
- `scaler.pkl` - Feature scaler

### Server Ports

- Backend: 8000 (configurable in `start_servers.py`)
- ML Server: 8001 (configurable in `ml_server/main.py`)

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Servers not starting? (Windows)

1. Check Python version: `py -3.11 --version` (requires 3.11)
2. Check logs: `type .\logs\backend.log`
3. Verify ports are free: `netstat -ano | findstr :8000` and `findstr :8001`
4. Kill lingering processes: `taskkill /PID <PID> /F`

### TensorFlow installation issues?

- **macOS (Apple Silicon)**: Use `tensorflow-macos` instead of `tensorflow`
- **Python 3.13**: Not supported - use Python 3.11

### Camera not working on device?

1. Ensure camera permissions are granted
2. Check that the app has access to front/back cameras
3. Restart the app with a cold restart (not hot reload)

### API connection errors?

1. Ensure phone and computer are on the **same WiFi network**
2. Update API URL in Flutter to your computer's IP: `http://YOUR_IP:8000`
3. Check firewall isn't blocking ports 8000/8001

### Model not found?

```bash
cd ml_server
ls -la model/
# Ensure sign_model.h5, label_map.json, scaler.pkl exist
```

### Virtual environment issues?

```bash
# Recreate venv
rm -rf backend/train_venv ml_server/venv_infer
python3.11 start_servers.py  # Will recreate automatically
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

Sunakshi Gawas - Main Developer

## 🙏 Acknowledgments

- MediaPipe for hand pose estimation
- TensorFlow for machine learning
- Flutter community for mobile development
- MyMemory API for translation services

## 📞 Support

For issues, questions, or suggestions:

1. Open an Issue on GitHub
2. Check existing documentation
3. Review the troubleshooting section

## 🚀 Future Enhancements

- [ ] Support for more sign languages (ASL, BSL, etc.)
- [ ] Offline mode with on-device ML inference
- [ ] Sentence-level sign detection
- [ ] Avatar-based 3D sign animations
- [ ] User authentication and sign history
- [ ] Web interface
- [ ] iOS App Store release
- [ ] Android Play Store release
- [ ] Two-way video calling with sign translation

---

<p align="center">
  <b>Made with ❤️ for the Deaf and Hard of Hearing community</b>
</p>
