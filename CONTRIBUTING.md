# Contributing to SignVerse AI

Thank you for your interest in contributing to SignVerse AI! This document provides guidelines and instructions for contributing.

## 📋 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on solutions, not blame
- Respect diverse perspectives

## 🎯 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Provide a clear description** of the bug
3. **Include steps to reproduce**
4. **Provide environment details**:
   - OS and Python version
   - Which component (app, backend, ML)
   - Error logs from `/tmp/backend.log` or `/tmp/ml_server.log`

**Example:**
```
Title: Backend crashes when processing invalid landmarks

Description:
When sending a POST request to /api/predict with malformed features array,
the backend crashes instead of returning an error.

Steps to reproduce:
1. Start servers with python3 start_servers.py
2. Send: curl -X POST http://localhost:8001/api/predict -d '{"features":[]}'
3. Backend logs show IndexError

Environment:
- macOS 13.0
- Python 3.11.0
- TensorFlow 2.12.0
```

### Suggesting Features

1. **Describe the feature** and its benefits
2. **Provide use cases** where it would be helpful
3. **Suggest implementation approach** if possible
4. **Consider existing architecture**

**Example:**
```
Title: Add offline mode for sign detection

Description:
Allow the app to work without internet by bundling the ML model locally.

Benefits:
- Works in areas without connectivity
- Faster inference (no network latency)
- Better privacy (data stays local)

Use cases:
- Rural areas with poor connectivity
- Classrooms and hospitals
- Users concerned about privacy
```

## 🔧 Development Setup

### Fork and Clone
```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Sign-Language.git
cd Sign-Language
git remote add upstream https://github.com/original-owner/Sign-Language.git
```

### Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or for bugs
git checkout -b fix/bug-description
```

### Install Dependencies
```bash
# Backend
cd backend
python3 -m venv train_venv
source train_venv/bin/activate
pip install -r requirements.txt

# ML Server
cd ../ml_server
python3 -m venv venv_infer
source venv_infer/bin/activate
pip install -r requirements.txt

# Flutter
cd ../sign_bridge
flutter pub get
```

### Start Development Servers
```bash
cd /path/to/Sign-Language
python3 start_servers.py
# In another terminal for Flutter:
cd sign_bridge
flutter run
```

## 📝 Commit Guidelines

- Use clear, descriptive commit messages
- Reference issue numbers: `Fix #123: Add offline mode`
- Keep commits focused and atomic
- Include tests for new features

**Good commit messages:**
```
Add sign language detection for ASL

- Extend label_map.json with ASL signs
- Update model training script
- Add ASL language support to backend

Fixes #42
```

## 🧪 Testing

Before submitting a PR:

1. **Test manually**:
```bash
# Start servers
python3 start_servers.py

# Test backend
curl http://localhost:8000/api/health

# Test ML server
curl -X POST http://localhost:8001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0]*63}'

# Test app
cd sign_bridge && flutter run
```

2. **Check logs**:
```bash
tail -f /tmp/backend.log
tail -f /tmp/ml_server.log
```

3. **Verify no regressions**:
- Existing signs still work
- Server starts cleanly
- Graceful shutdown works
- No new warnings

## 📤 Submitting a Pull Request

1. **Update main branch**:
```bash
git fetch upstream
git rebase upstream/main
```

2. **Push your branch**:
```bash
git push origin feature/your-feature-name
```

3. **Open PR on GitHub** with:
   - Clear title describing changes
   - Description of what and why
   - Reference to related issues
   - Screenshots for UI changes
   - Testing verification

**PR Template:**
```markdown
## Description
Brief summary of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation

## Related Issues
Fixes #123

## Testing Done
- [x] Manual testing
- [x] Verified no regressions
- [x] Tested on device

## Screenshots (if applicable)
[Add before/after or feature screenshots]

## Checklist
- [x] Code follows style guidelines
- [x] Commits are descriptive
- [x] No debug code or console.logs
- [x] Tested thoroughly
```

## 🎨 Code Style

### Python
- Follow PEP 8
- Use meaningful variable names
- Add docstrings for functions
- Keep functions focused and small

```python
def detect_sign(landmarks: List[float]) -> Dict[str, Any]:
    """
    Detect sign from hand landmarks.
    
    Args:
        landmarks: 63-dimensional hand landmark vector
        
    Returns:
        Dictionary with sign label, index, and confidence
    """
    # Implementation
```

### Dart/Flutter
- Follow Dart style guide
- Use meaningful widget names
- Add comments for complex logic
- Use const constructors when possible

```dart
class SignDetectionScreen extends StatefulWidget {
  /// Main screen for real-time sign detection
  
  @override
  State<SignDetectionScreen> createState() => _SignDetectionScreenState();
}
```

### Commit Messages
- Start with verb: Add, Fix, Update, Remove, Refactor
- Be specific and clear
- Keep subject under 50 characters
- Reference issues when applicable

## 📚 Documentation

When adding features, update documentation:
- README.md (user-facing)
- Code comments (technical details)
- Docstrings (function documentation)
- CONTRIBUTING.md (this file, if needed)

## 🚀 Development Workflow

1. **Create issue** for discussion (optional but recommended)
2. **Fork the repo** and create feature branch
3. **Make changes** with clear commits
4. **Test thoroughly** before pushing
5. **Open PR** with detailed description
6. **Address feedback** from reviewers
7. **Merge** after approval

## 📞 Questions?

- Check existing issues and PRs
- Review README and documentation
- Open a discussion on GitHub
- Reach out to maintainers

## ⭐ Getting Help

- **Stuck on setup?** Check troubleshooting in README
- **Model questions?** See backend/train_sign_model.py
- **UI issues?** Check sign_bridge/lib/screens/
- **API questions?** See backend/app/main.py

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [Flutter Documentation](https://flutter.dev/docs)
- [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)

## 🙏 Thank You!

Your contributions help make sign language technology more accessible to everyone. Thank you for being part of this mission!

---

**Happy Contributing! 🚀**
