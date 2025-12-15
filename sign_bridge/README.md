# SignVerse AI - Flutter Mobile App

Cross-platform mobile application for real-time sign language recognition and translation. Built with Flutter to support iOS, Android, and Web platforms.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Directory Structure](#directory-structure)
- [Setup & Installation](#setup--installation)
- [Running the App](#running-the-app)
- [Architecture](#architecture)
- [Features Guide](#features-guide)
- [Building for Release](#building-for-release)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

SignVerse AI is a real-time sign language recognition app that:
- Captures video from device camera
- Extracts hand landmarks using MediaPipe
- Sends to backend for sign recognition
- Displays recognized signs with animations
- Provides text-to-sign translation
- Offers text-to-speech for accessibility
- Works offline with cached models
- Supports 11+ sign languages

### Target Platforms
- **Android**: 5.0+ (API 21+)
- **iOS**: 12.0+
- **Web**: Modern browsers (Chrome, Safari, Firefox)

### Key Technologies
- **Framework**: Flutter 3.13+
- **Language**: Dart
- **State Management**: Provider
- **Backend Communication**: HTTP, WebSocket
- **Camera**: Camera plugin
- **ML Integration**: MediaPipe (via backend)
- **UI**: Material Design 3

## ✨ Features

### Core Features
- 📹 **Real-time Camera Capture** - Live video feed from device
- 🤖 **AI Sign Recognition** - ML-powered hand pose detection
- 🎯 **Gesture Recognition** - Multi-frame sign detection
- 📝 **Text-to-Sign Translation** - Convert text to sign animations
- 🔊 **Text-to-Speech** - Audio output for translations
- 💾 **Offline Mode** - Cached models and signs
- 🎨 **Animated GIFs** - Visual representation of signs
- 🌍 **Multi-language** - Support for multiple sign languages
- ♿ **Accessibility** - Screen reader support, TTS
- 📊 **History** - Translation history tracking
- 🎬 **Video Playback** - Recorded sign demonstrations

### User Interface
- Clean, intuitive Material Design 3
- Bottom navigation for feature access
- Real-time camera preview with overlay
- Gesture feedback and animations
- Responsive layout for all screen sizes
- Dark/Light theme support

## 💻 Tech Stack

### Frontend Framework
- **Flutter** (3.13+) - Multi-platform mobile development
- **Dart** - Programming language
- **Material Design 3** - UI components and design system

### State Management
- **Provider** (6.1.0+) - Simple, powerful state management
- Alternatives: Riverpod, BLoC (can be swapped)

### Networking
- **HTTP** (1.2.0+) - REST API communication
- **WebSocket** (optional) - Real-time bidirectional communication
- **URL Launcher** (6.3.0+) - Deep linking and external URLs

### Camera & Media
- **Camera** (0.11.0+) - Device camera access
- **Video Player** (2.9.1+) - Video playback
- **Permission Handler** (11.3.0+) - Runtime permissions
- **Image Picker** (optional) - Gallery image selection

### ML & Processing
- **MediaPipe** (via backend) - Hand landmark detection
- **TensorFlow** (inference via backend) - Sign classification

### Accessibility & User Experience
- **Flutter TTS** (4.0.2+) - Text-to-speech functionality
- **Cupertino Icons** (1.0.8+) - iOS-style icons
- **WebView Flutter** (4.10.0+) - Embedded web content

### Development Tools
- **Flutter Launcher Icons** (0.14.4+) - App icon generation
- **Dart Analysis** - Code linting and analysis

## 📁 Directory Structure

```
sign_bridge/
│
├── 📚 Documentation
│   ├── README.md                  # This file
│   ├── ARCHITECTURE.md            # App architecture & patterns
│   ├── DEVELOPMENT.md             # Development guide
│   └── BUILD.md                   # Build & release guide
│
├── 🎨 UI & Assets
│   ├── assets/                    # Images, icons, GIFs, fonts
│   │   ├── icons/
│   │   ├── images/
│   │   ├── gifs/
│   │   └── fonts/
│   │
│   ├── lib/
│   │   ├── main.dart              # App entry point
│   │   ├── widgets/               # Reusable UI widgets
│   │   ├── screens/               # Full screen pages
│   │   │   ├── home_screen.dart
│   │   │   ├── camera_screen.dart
│   │   │   ├── translate_screen.dart
│   │   │   ├── history_screen.dart
│   │   │   └── settings_screen.dart
│   │   └── services/              # API & business logic
│   │       ├── api_service.dart
│   │       ├── ml_service.dart
│   │       ├── camera_service.dart
│   │       ├── storage_service.dart
│   │       └── notification_service.dart
│
├── 🔧 Configuration
│   ├── pubspec.yaml               # Dependencies
│   ├── pubspec.lock               # Locked versions
│   ├── analysis_options.yaml      # Lint rules
│   ├── .gitignore                 # Git ignore patterns
│   └── .env                       # Environment variables
│
├── 🏗️ Platform-Specific
│   ├── android/                   # Android native code
│   │   ├── app/
│   │   ├── build.gradle
│   │   └── AndroidManifest.xml
│   │
│   ├── ios/                       # iOS native code
│   │   ├── Runner/
│   │   ├── Podfile
│   │   └── Info.plist
│   │
│   ├── web/                       # Web platform
│   │   ├── index.html
│   │   └── manifest.json
│   │
│   ├── linux/                     # Linux platform
│   ├── macos/                     # macOS platform
│   └── windows/                   # Windows platform
│
├── 🧪 Testing
│   └── test/
│       └── widget_test.dart
│
└── 📦 Build Output
    └── build/
```

## 🚀 Setup & Installation

### Prerequisites

- **Flutter SDK** (3.13+)
  ```bash
  flutter --version
  ```
- **Dart SDK** (included with Flutter)
- **Platform Tools**
  - Android: Android SDK 21+, Android Studio
  - iOS: Xcode 12+, iOS 12+
- **Backend Servers** Running on:
  - Backend: `http://localhost:8000`
  - ML Server: `http://localhost:8001`

### Quick Start

**1. Get Flutter**
```bash
# Install Flutter from https://flutter.dev/docs/get-started/install
# Or update existing installation
flutter upgrade
```

**2. Navigate to App Directory**
```bash
cd sign_bridge
```

**3. Get Dependencies**
```bash
flutter pub get
```

**4. Run App (Development)**
```bash
# List available devices
flutter devices

# Run on default device
flutter run

# Run on specific device
flutter run -d <device-id>
```

### Manual Setup (Detailed)

**For Android:**
```bash
cd sign_bridge

# Get dependencies
flutter pub get

# Run on Android device/emulator
flutter run -d android
```

**For iOS:**
```bash
cd sign_bridge

# Get dependencies
flutter pub get

# Install pod dependencies
cd ios
pod install
cd ..

# Run on iOS device/simulator
flutter run -d ios
```

**For Web:**
```bash
cd sign_bridge

# Get dependencies
flutter pub get

# Run web version
flutter run -d chrome
```

## 🏃 Running the App

### Development Mode

```bash
# Hot reload enabled (changes reflected instantly)
flutter run

# With verbose logging
flutter run -v

# With profiling
flutter run --profile

# With specific device
flutter run -d <device-id>
```

### Debug Mode

```bash
# Full debugging with breakpoints, etc.
flutter run --debug
```

### Release Mode

```bash
# Optimized, no debugging
flutter run --release
```

### Run with Options

```bash
# Skip build, just run
flutter run --no-build

# Use specific flavor
flutter run --flavor production

# Pass arguments
flutter run -- --enable-tts
```

## 🏛️ Architecture

### App Structure

```
┌─────────────────────────────────────┐
│         main.dart                   │
│  (App initialization & routing)     │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────────┐  ┌─────────────┐
│  Providers  │  │   Routes    │
│  (State)    │  │  (Navigation)│
└────┬────────┘  └─────┬───────┘
     │                 │
     ▼                 ▼
┌──────────────────────────────────┐
│         Screens (Pages)          │
├──────────────────────────────────┤
│ - HomeScreen                     │
│ - CameraScreen                   │
│ - TranslateScreen                │
│ - HistoryScreen                  │
│ - SettingsScreen                 │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│      Services (Business Logic)   │
├──────────────────────────────────┤
│ - ApiService (HTTP)              │
│ - MLService (ML inference)       │
│ - CameraService (Camera control) │
│ - StorageService (Local storage) │
│ - NotificationService (Alerts)   │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│       Backend Servers            │
├──────────────────────────────────┤
│ - Backend (port 8000)            │
│ - ML Server (port 8001)          │
└──────────────────────────────────┘
```

### State Management (Provider)

```dart
// Define providers
final signProvider = Provider<String>((ref) => "");
final translationProvider = StateNotifierProvider<TranslationNotifier, String>(
  (ref) => TranslationNotifier(),
);

// Use in widgets
@override
Widget build(BuildContext context, WidgetRef ref) {
  final sign = ref.watch(signProvider);
  return Text(sign);
}
```

## 📱 Features Guide

### 1. Real-Time Camera Screen
- Displays live camera feed
- Shows detected hand landmarks
- Displays current sign with confidence
- Real-time feedback with haptics
- Confidence threshold indicator

### 2. Text-to-Sign Translation
- Enter text to translate
- View animated sign sequence
- Play audio (TTS)
- Save to history
- Share translations

### 3. Translation History
- View past translations
- Search and filter
- Delete individual entries
- Export history
- Offline access

### 4. Settings
- API endpoint configuration
- Confidence threshold adjustment
- Language selection
- Theme (Dark/Light)
- TTS settings
- Permission management

## 🔨 Building for Release

### Android Release

```bash
cd sign_bridge

# Build APK
flutter build apk --release

# Build App Bundle (for Play Store)
flutter build appbundle --release

# Outputs:
# APK: build/app/outputs/apk/release/app-release.apk
# AAB: build/app/outputs/bundle/release/app-release.aab
```

### iOS Release

```bash
cd sign_bridge

# Build iOS app
flutter build ios --release

# Build for submission
flutter build ipa --release

# Output: build/ios/ipa/SignVerse.ipa
```

### Web Release

```bash
cd sign_bridge

# Build web version
flutter build web --release

# Output: build/web/
# Deploy to any web host
```

## 🐛 Troubleshooting

### Setup Issues

**Flutter not found**
```bash
# Add Flutter to PATH
export PATH="$PATH:/path/to/flutter/bin"

# Verify installation
flutter doctor
```

**Pub get fails**
```bash
# Clear pub cache
flutter pub cache clean

# Get fresh dependencies
flutter pub get
```

### Runtime Issues

**Camera permission denied**
```
Solution: Check permissions in settings
- Android: Settings > Permissions
- iOS: Settings > SignVerse > Camera
```

**Connection to backend fails**
```
Solution: Ensure backend servers are running
- Backend: python3 start_servers.py
- Check network connectivity
- Verify API endpoint in settings
```

**Slow performance on older devices**
```
Solutions:
- Use lower camera resolution
- Reduce frame rate
- Enable profile mode: flutter run --profile
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "SDK constraints" | Flutter version mismatch | `flutter upgrade` |
| "Pod install" fails | CocoaPods issue (iOS) | `flutter clean && flutter pub get` |
| "Build failed" | Gradle/Xcode error | `flutter clean` |
| "No devices found" | No emulator/device running | `flutter devices` |

## 📚 Additional Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Dart Language Guide](https://dart.dev/guides)
- [Provider Documentation](https://pub.dev/packages/provider)
- [Material Design 3](https://m3.material.io/)
- [Firebase Integration](https://firebase.flutter.dev/)

## 🤝 Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Mobile App-Specific Guidelines

1. **Always test on physical devices** before committing
2. **Check platform-specific code** (Android/iOS differences)
3. **Use proper null safety** (?) throughout
4. **Add error handling** for network requests
5. **Test permissions** for camera/microphone
6. **Follow Material Design 3** patterns
7. **Optimize performance** (hot reload, profiling)
8. **Document complex logic** with comments

## 📝 License

MIT License - See [../LICENSE](../LICENSE)

---

**Last Updated**: December 15, 2025  
**Flutter Version**: 3.13+  
**Dart Version**: 3.10+
