# SignVerse AI - Real-Time Sign Language Translation

A mobile app and server infrastructure for real-time sign language detection and translation to text and speech in multiple languages.

## 🎯 Features

- **Real-time Sign Detection**: Uses MediaPipe for hand landmark detection
- **AI-powered Classification**: TensorFlow-based sign classifier trained on 11+ sign classes
- **Multi-language Support**: English and Marathi translations
- **Text-to-Speech**: Natural audio output with multiple voice options
- **Cross-platform**: Android mobile app with Flutter
- **REST API**: Easy integration with FastAPI backend

## 📱 Supported Signs

- BEST
- DISLIKE
- HELLO
- NO
- OK
- PEACE
- ROCK
- SORRY
- THANK
- YES
- YOU

## 🏗️ Architecture

```
Sign-Language/
├── sign_bridge/          # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/      # UI screens
│   │   ├── services/     # API clients
│   │   └── widgets/      # Reusable components
│   ├── android/          # Android native code
│   └── ios/              # iOS native code
│
├── backend/              # FastAPI Backend (Port 8000)
│   ├── app/
│   │   ├── main.py       # FastAPI app entry
│   │   ├── schemas.py    # Request/response schemas
│   │   └── services/     # Business logic
│   ├── requirements.txt
│   └── train_venv/       # Python virtual environment
│
├── ml_server/            # TensorFlow ML Server (Port 8001)
│   ├── main.py           # ML server entry
│   ├── model/            # Trained models & label maps
│   │   ├── sign_model.h5
│   │   ├── label_map.json
│   │   └── scaler.pkl
│   └── venv_infer/       # Python virtual environment
│
└── start_servers.py      # One-command startup script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip and venv
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sign-language.git
cd Sign-Language
```

2. **Start Backend & ML Server (Recommended)**
```bash
python3 start_servers.py
```

The script will:
- Activate virtual environments automatically
- Start Backend API on `http://localhost:8000`
- Start ML Server on `http://localhost:8001`
- Monitor both servers continuously
- Stop gracefully with `Ctrl+C`

### Manual Setup (Alternative)

**Backend Server:**
```bash
cd backend
python3 -m venv train_venv
source train_venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**ML Server:**
```bash
cd ml_server
python3 -m venv venv_infer
source venv_infer/bin/activate
pip install -r requirements.txt
python3 main.py
```

**Flutter App:**
```bash
cd sign_bridge
flutter pub get
flutter run
```

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

### Sign Detection
```bash
POST http://localhost:8001/api/predict
Content-Type: application/json

{
  "features": [0.0, 0.1, ...]  // 63-dimensional hand landmarks
}
```

### Text Translation
```bash
GET http://localhost:8000/api/translate?text=Hello&language=mr
```

## 🎓 Model Training

The sign classifier model was trained on hand landmark data collected from video recordings using:
- **Feature Extraction**: MediaPipe Hand Pose (21 landmarks × 3 coordinates = 63 features)
- **Model**: TensorFlow Sequential model
- **Preprocessing**: StandardScaler normalization
- **Classes**: 11 sign categories

To retrain:
```bash
cd backend
python3 train_sign_model.py
```

## 🛠️ Development

### Project Structure
- **Frontend**: Flutter (Dart) - Real-time camera capture, UI
- **Backend**: FastAPI (Python) - REST API, business logic
- **ML**: TensorFlow (Python) - Model inference, predictions
- **Data**: Training datasets in `backend/data/` directory

### Testing Servers
```bash
# Check backend
curl -s http://localhost:8000/api/health | jq .

# Check ML server
curl -s http://localhost:8001/api/predict \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"features": [0]*63}'
```

### Logs
- Backend logs: `/tmp/backend.log`
- ML Server logs: `/tmp/ml_server.log`

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

### Servers not starting?
1. Check Python version: `python3 --version` (requires 3.9+)
2. Check logs: `tail -f /tmp/backend.log`
3. Verify ports are free: `lsof -i :8000,:8001`
4. Kill lingering processes: `pkill -f "uvicorn\|main.py"`

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
python3 start_servers.py  # Will recreate automatically
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Soham Bamane** - Main Developer

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

- [ ] Support for more sign languages (ASL, ISL, etc.)
- [ ] Offline mode with cached models
- [ ] Real-time video processing improvements
- [ ] Database for sign history
- [ ] User authentication and profiles
- [ ] Web interface
- [ ] iOS app release
- [ ] Gesture recognition improvements

---

**Made with ❤️ for the Deaf and Hard of Hearing community**
