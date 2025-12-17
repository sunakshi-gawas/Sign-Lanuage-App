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

- Captures video from device camera (front/back toggle)
- Extracts hand landmarks using MediaPipe
- Sends to backend for sign recognition
- Displays recognized signs with confidence scores
- Provides text-to-sign translation with GIF animations
- Shows real-time online/offline network status
- Features modern purple & orange themed UI
- Supports 9 sign gestures

### Target Platforms

- **Android**: 5.0+ (API 21+)
- **iOS**: 12.0+
- **Web**: Modern browsers (Chrome, Safari, Firefox)

### Key Technologies

- **Framework**: Flutter 3.10+
- **Language**: Dart 3.10+
- **State Management**: Provider 6.1.0
- **Backend Communication**: HTTP
- **Camera**: Camera plugin 0.11.0
- **Network Detection**: connectivity_plus
- **UI**: Material Design 3 with custom theming

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
- **Dart** (3.10+) - Programming language
- **Material Design 3** - UI components with custom theming

### State Management

- **Provider** (6.1.0) - Simple, powerful state management

### Networking

- **HTTP** (1.2.0) - REST API communication
- **connectivity_plus** (6.0.3) - Real-time network status detection
- **URL Launcher** (6.3.0) - External URLs

### Camera & Media

- **Camera** (0.11.0) - Device camera access with front/back toggle
- **Video Player** (2.9.1) - Video playback
- **Permission Handler** (11.3.0) - Runtime permissions

### Accessibility & User Experience

- **Flutter TTS** (4.0.2) - Text-to-speech functionality
- **Cupertino Icons** (1.0.8) - iOS-style icons
- **WebView Flutter** (4.10.0) - Embedded web content

### Development Tools

- **Flutter Launcher Icons** (0.14.4) - App icon generation
- **Flutter Lints** - Code analysis

## 📁 Directory Structure

```
sign_bridge/
│
├── lib/                           # Dart source code
│   ├── main.dart                  # App entry point & providers
│   │
│   ├── screens/                   # Full screen pages
│   │   ├── home_screen.dart       # Main dashboard with online status
│   │   ├── sign_to_text_screen_v2.dart  # Camera-based sign detection
│   │   └── text_to_sign_screen.dart     # Text to GIF translation
│   │
│   ├── services/                  # API & business logic
│   │   ├── api_client.dart        # HTTP client for backend
│   │   └── server_discovery.dart  # Auto-discover server IP
│   │
│   ├── theme/                     # App theming
│   │   └── app_theme.dart         # Purple/orange color scheme
│   │
│   └── widgets/                   # Reusable UI widgets
│       └── rounded_button.dart    # Custom button component
│
├── assets/                        # Static assets
│   └── logo.png                   # App logo
│
├── android/                       # Android native code
│   ├── app/build.gradle.kts
│   └── ...
│
├── ios/                           # iOS native code
│   ├── Runner/
│   └── ...
│
├── web/                           # Web platform
│   ├── index.html
│   └── manifest.json
│
├── linux/                         # Linux platform
├── macos/                         # macOS platform
├── windows/                       # Windows platform
│
├── test/                          # Unit & widget tests
│   └── widget_test.dart
│
├── pubspec.yaml                   # Dependencies
├── pubspec.lock                   # Locked versions
├── analysis_options.yaml          # Lint rules
└── README.md                      # This file
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
// Define a ChangeNotifier for app state
class TranslationNotifier extends ChangeNotifier {
  String _text = "";
  String get text => _text;

  void setText(String value) {
    _text = value;
    notifyListeners();
  }
}

// Provide it at app root (in main.dart)
MultiProvider(
  providers: [
    ChangeNotifierProvider(create: (_) => TranslationNotifier()),
  ],
  child: const MyApp(),
);

// Consume in widgets
@override
Widget build(BuildContext context) {
  final text = context.watch<TranslationNotifier>().text;
  return Text(text);
}
```

## 📱 Features Guide

### 1. Home Screen (`home_screen.dart`)

- App logo and branding
- Real-time online/offline status indicator
- Feature cards for navigation
- Purple & orange gradient hero section
- Quick access to Sign-to-Text and Text-to-Sign

### 2. Sign to Text (`sign_to_text_screen_v2.dart`)

- Live camera feed with aspect ratio correction
- Front/back camera toggle button
- Real-time hand landmark detection
- Sign prediction with confidence percentage
- Unknown gesture handling (< 70% confidence)
- Gradient purple border around camera
- Settings dialog for camera options

### 3. Text to Sign (`text_to_sign_screen.dart`)

- Text input with orange-themed styling
- Convert button with gradient design
- Animated GIF display for signs
- Token display showing parsed signs
- Navigation controls (prev/next)
- Page indicators for multiple signs
- Empty state with instructions

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
- Backend: py -3.11 start_servers.py
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

| Error               | Cause                      | Solution                           |
| ------------------- | -------------------------- | ---------------------------------- |
| "SDK constraints"   | Flutter version mismatch   | `flutter upgrade`                  |
| "Pod install" fails | CocoaPods issue (iOS)      | `flutter clean && flutter pub get` |
| "Build failed"      | Gradle/Xcode error         | `flutter clean`                    |
| "No devices found"  | No emulator/device running | `flutter devices`                  |

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

**Last Updated**: December 16, 2025  
**Flutter Version**: 3.13+  
**Dart Version**: 3.10+  
**Maintainer**: XXXXXXXXX
