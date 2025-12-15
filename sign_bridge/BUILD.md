# Flutter App Build & Release Guide

Complete guide to building, testing, and releasing the SignVerse AI app on Android, iOS, and Web platforms.

## 📋 Table of Contents

- [Pre-Release Checklist](#pre-release-checklist)
- [Android Release](#android-release)
- [iOS Release](#ios-release)
- [Web Release](#web-release)
- [Testing Before Release](#testing-before-release)
- [Play Store Deployment](#play-store-deployment)
- [App Store Deployment](#app-store-deployment)
- [Troubleshooting](#troubleshooting)

## ✅ Pre-Release Checklist

```
□ Version number updated (pubspec.yaml)
□ Build number incremented
□ All tests passing (flutter test)
□ No warnings or errors (flutter analyze)
□ App icons updated (flutter pub run flutter_launcher_icons:main)
□ Splash screen configured
□ Firebase configured (if using)
□ API endpoints verified
□ Permissions configured (Android/iOS)
□ Privacy policy prepared
□ App description prepared
□ Screenshots captured (Play Store/App Store)
□ Release notes written
□ Changelog updated
```

## 🤖 Android Release

### Setup

**1. Generate Keystore**
```bash
keytool -genkey -v -keystore ~/sign_bridge.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias sign_bridge

# Enter password and key information
```

**2. Create Key Properties File**
```bash
# android/key.properties
storePassword=<password>
keyPassword=<password>
keyAlias=sign_bridge
storeFile=/Users/username/sign_bridge.jks
```

**3. Configure Gradle**
```bash
# android/app/build.gradle
android {
    ...
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile file(keystoreProperties['storeFile'])
            storePassword keystoreProperties['storePassword']
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

### Build APK

```bash
cd sign_bridge

# Clean previous builds
flutter clean

# Get dependencies
flutter pub get

# Build APK
flutter build apk --release

# Output
# build/app/outputs/apk/release/app-release.apk

# Build split APKs (for different architectures)
flutter build apk --split-per-abi --release

# Outputs:
# build/app/outputs/apk/release/app-armeabi-v7a-release.apk
# build/app/outputs/apk/release/app-arm64-v8a-release.apk
# build/app/outputs/apk/release/app-x86_64-release.apk
```

### Build App Bundle

```bash
cd sign_bridge

# Build App Bundle (for Play Store)
flutter build appbundle --release

# Output
# build/app/outputs/bundle/release/app-release.aab

# Verify bundle
bundletool build-apks \
  --bundle=build/app/outputs/bundle/release/app-release.aab \
  --output=sign_bridge.apks \
  --ks=~/sign_bridge.jks \
  --ks-pass=pass:<password> \
  --ks-key-alias=sign_bridge \
  --key-pass=pass:<password>
```

### Test APK

```bash
# Install APK on device
adb install build/app/outputs/apk/release/app-release.apk

# Or with bundletool
bundletool install-apks --apks=sign_bridge.apks
```

### Update Version

```yaml
# pubspec.yaml
version: 1.0.0+1

# For next release:
# - Increment version: 1.0.0+1 → 1.1.0+2
# - Change: 1.0.0+1 (version+buildNumber)
```

## 🍎 iOS Release

### Setup

**1. Configure App ID**
```bash
# Open in Xcode
open ios/Runner.xcworkspace

# In Xcode:
# - Set Bundle ID (com.yourname.signverse)
# - Set Team ID
# - Enable capabilities (Camera, Microphone)
```

**2. Create Provisioning Profile**
- Go to Apple Developer Account
- Create App ID matching Bundle ID
- Create Production Provisioning Profile
- Download and add to Xcode

**3. Update Build Settings**
```bash
# In Xcode
# Runner > Build Settings
# Set:
# - Code Sign Identity: iOS Distribution
# - Provisioning Profile: select profile
# - Version: 1.0.0
# - Build: 1
```

### Build iOS App

```bash
cd sign_bridge

# Clean
flutter clean

# Get dependencies
flutter pub get

# Build for device
flutter build ios --release

# Output
# build/ios/iphoneos/Runner.app
```

### Archive for App Store

```bash
cd sign_bridge/ios

# Open workspace
open Runner.xcworkspace

# In Xcode:
# 1. Select "Generic iOS Device" or your device
# 2. Product > Archive
# 3. Organizer window opens
# 4. Select archive > Distribute App
# 5. Select "App Store Connect" > Next
# 6. Complete signing options
# 7. Upload

# Or from command line:
xcodebuild -workspace Runner.xcworkspace \
  -scheme Runner -configuration Release \
  -derivedDataPath build/ -archivePath \
  build/Runner.xcarchive archive

xcodebuild -exportArchive \
  -archivePath build/Runner.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/
```

### Create Export Options

```xml
# ios/ExportOptions.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" ...>
<plist version="1.0">
<dict>
  <key>method</key>
  <string>app-store</string>
  <key>signingStyle</key>
  <string>automatic</string>
  <key>stripSwiftSymbols</key>
  <true/>
  <key>teamID</key>
  <string>YOUR_TEAM_ID</string>
</dict>
</plist>
```

## 🌐 Web Release

### Build Web

```bash
cd sign_bridge

# Clean
flutter clean

# Get dependencies
flutter pub get

# Build web
flutter build web --release

# Output
# build/web/

# Optimized build (smaller size)
flutter build web --release \
  --web-renderer html \
  --dart2js-optimization O4
```

### Deploy to GitHub Pages

```bash
# Build web
flutter build web --release

# Copy to docs folder (if using docs/)
cp -r build/web/* docs/

# Commit and push
git add docs/
git commit -m "Deploy web version"
git push origin main
```

### Deploy to Firebase Hosting

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize Firebase
firebase init hosting

# Build and deploy
flutter build web --release
firebase deploy --only hosting
```

### Deploy to Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
flutter build web --release
netlify deploy --prod --dir=build/web
```

## 🧪 Testing Before Release

### Functionality Testing

```
□ Camera works on physical device
□ Signs recognized correctly
□ Text-to-speech works
□ Translation API responds
□ Navigation works smoothly
□ All buttons/gestures work
□ Offline mode works (if implemented)
□ History saved correctly
□ Settings persist
□ No crashes or errors
```

### Performance Testing

```bash
# Profile app
flutter run --profile

# Check memory usage
# In DevTools > Memory

# Check CPU usage
# In DevTools > CPU Profiler

# Frame rate
# In DevTools > Performance

# Typical good metrics:
# - Frame rate: 50-60 FPS
# - Memory: < 100MB
# - Jank: < 5%
```

### Permissions Testing

```
□ Camera permission requested
□ Microphone permission (if needed)
□ Storage permission (if needed)
□ Location permission (if needed)
□ Handle permission denial gracefully
```

### Device Testing

```
Test on multiple devices:
□ Android: minimum version (API 21+)
□ Android: high-end device
□ Android: low-end device
□ iOS: minimum version (iOS 12+)
□ iOS: latest version
□ Web: Chrome, Safari, Firefox
```

## 📱 Play Store Deployment

### Prepare App

```
1. Create Google Play account
2. Set up store listing
3. Prepare screenshots
4. Write description and release notes
5. Set content rating
6. Set privacy policy URL
7. Configure pricing and distribution
```

### Upload App Bundle

```bash
# Build release bundle
flutter build appbundle --release

# Sign bundle (already signed if using gradle)

# Upload via Play Console:
# 1. Go to Google Play Console
# 2. Select app > Release > Create release
# 3. Select App Bundle (.aab) file
# 4. Upload build/app/outputs/bundle/release/app-release.aab
# 5. Review and publish
```

### Rollout Strategy

```
1. Internal Testing (QA team)
2. Closed Testing (selected users)
3. Open Testing (more users)
4. Production Rollout (all users)
   - Start with 10%
   - Increase to 25%, 50%, 100%
   - Monitor crash rates and ratings
```

## 🍎 App Store Deployment

### Prepare App

```
1. Create Apple Developer account
2. Set up App Store Connect
3. Create app record
4. Fill app information
5. Add screenshots
6. Write description
7. Set keywords and category
8. Add privacy policy
9. Configure pricing
```

### Submit to App Store

```bash
# Build and archive
flutter build ios --release

# In Xcode:
# Product > Archive
# Organizer > Select archive
# Distribute App > App Store Connect

# Or use Transporter:
# Xcode > Organizer > Export > Save for distribution
# Open Transporter app
# Drag and drop .ipa file
# Submit
```

### Approval Process

```
1. Binary upload → Review in progress (1-3 days)
2. MetaData review
3. Testing phase
4. App Review approval
5. Prepare for Release
6. Release to App Store
```

## 🐛 Troubleshooting

### Build Failures

| Error | Cause | Solution |
|-------|-------|----------|
| "No provisioning profiles" | Missing iOS cert | Re-download provisioning profile from Apple |
| "Build version mismatch" | pubspec.yaml not updated | Update version in pubspec.yaml |
| "Pod install fails" | CocoaPods cache | `cd ios && pod deintegrate && pod install` |
| "Gradle build fails" | Java version | Ensure Java 11+ is installed |

### Runtime Issues

| Issue | Solution |
|-------|----------|
| Crash on startup | Check logs: `flutter logs` |
| Slow performance | Profile app: `flutter run --profile` |
| Camera not working | Check permissions in device settings |
| API connection fails | Verify backend is running and accessible |

### Store Submission Issues

| Issue | Solution |
|-------|----------|
| App rejected for privacy | Add privacy policy URL |
| App rejected for permissions | Only request necessary permissions |
| Version not compatible | Check minimum SDK versions |
| Binary too large | Use App Bundle instead of APK |

## 📝 Release Checklist

```
Before Release:
□ Bump version number
□ Update CHANGELOG.md
□ Run tests: flutter test
□ Run analyzer: flutter analyze
□ Build all platforms
□ Test on physical devices
□ Check all permissions
□ Verify API endpoints
□ Update app icons/splash

During Release:
□ Create release notes
□ Take screenshots
□ Fill store listings
□ Set up pricing/distribution
□ Upload binaries

After Release:
□ Monitor crash reports
□ Check user ratings
□ Monitor analytics
□ Respond to user feedback
□ Plan next update
```

---

**Last Updated**: December 15, 2025  
**Flutter Version**: 3.13+
