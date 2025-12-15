# Flutter Development Guide

Complete guide to developing features, best practices, and workflow for the SignVerse AI Flutter app.

## 📋 Table of Contents

- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Writing Code](#writing-code)
- [Testing](#testing)
- [Debugging](#debugging)
- [Performance Profiling](#performance-profiling)
- [Common Tasks](#common-tasks)

## 🔧 Development Environment

### Setup

```bash
# Install Flutter
flutter pub global activate fvm  # Flutter Version Manager (optional)

# Verify installation
flutter doctor

# Install dependencies
cd sign_bridge
flutter pub get

# Generate code (if needed)
flutter pub run build_runner build
```

### IDE Setup

**VS Code**
```bash
# Install extensions
- Flutter (Dart Code)
- Dart (Dart Code)
- Provider Snippets
```

**Android Studio**
```
- Preferences > Plugins > Search "Flutter"
- Install Flutter and Dart plugins
```

## 📁 Project Structure Review

```
lib/
├── main.dart                 # Entry point
├── models/                   # Data classes
├── providers/                # State management
├── services/                 # Business logic
├── screens/                  # Full pages
├── widgets/                  # Reusable components
├── routes/                   # Navigation
├── constants/                # Constants
├── utils/                    # Helpers
├── theme/                    # Styling
└── config/                   # Configuration
```

## 🔄 Development Workflow

### Feature Development Steps

**1. Create Feature Branch**
```bash
git checkout -b feature/new-feature
```

**2. Create Models** (if needed)
```dart
// lib/models/feature_model.dart
class FeatureModel {
  final String id;
  final String name;
  
  FeatureModel({required this.id, required this.name});
  
  factory FeatureModel.fromJson(Map<String, dynamic> json) => 
    FeatureModel(id: json['id'], name: json['name']);
}
```

**3. Create Providers** (state management)
```dart
// lib/providers/feature_provider.dart
final featureProvider = StateNotifierProvider<FeatureNotifier, FeatureState>(
  (ref) => FeatureNotifier(),
);

class FeatureNotifier extends StateNotifier<FeatureState> {
  FeatureNotifier() : super(FeatureState());
  
  void doSomething() {
    state = state.copyWith(/* new state */);
  }
}
```

**4. Create Services** (API/business logic)
```dart
// lib/services/feature_service.dart
class FeatureService {
  Future<List<Feature>> fetchFeatures() async {
    // Implementation
  }
}
```

**5. Create Screens** (UI)
```dart
// lib/screens/feature_screen.dart
class FeatureScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(featureProvider);
    
    return Scaffold(
      appBar: AppBar(title: const Text('Feature')),
      body: Center(child: Text('Feature Content')),
    );
  }
}
```

**6. Create Widgets** (reusable components)
```dart
// lib/widgets/feature_widget.dart
class FeatureWidget extends StatelessWidget {
  final Feature feature;
  
  const FeatureWidget({required this.feature});
  
  @override
  Widget build(BuildContext context) {
    return Card(child: Text(feature.name));
  }
}
```

**7. Test Feature** (locally)
```bash
flutter run
# Test on device/emulator
```

**8. Commit & Push**
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

## 💻 Writing Code

### Dart/Flutter Best Practices

**1. Use const Constructors**
```dart
// ✅ Good
const SizedBox(height: 16.0)

// ❌ Avoid
SizedBox(height: 16.0)
```

**2. Proper Null Safety**
```dart
// ✅ Good
String? nullable;
String required;

// ❌ Avoid
String? nullable = null;
String? required;
```

**3. Follow Naming Conventions**
```dart
// ✅ Classes: PascalCase
class UserModel {}

// ✅ Variables/functions: camelCase
var userName = 'John';
void getUserName() {}

// ✅ Constants: camelCase
const maxRetries = 3;
```

**4. Add Documentation**
```dart
/// Fetches user data from the API
/// 
/// Returns a [Future<User>] that completes when data is received
/// 
/// Throws [HttpException] if the request fails
Future<User> getUser(String id) async {
  // Implementation
}
```

### Code Organization

```dart
// Order of declarations in a class:
class MyWidget extends StatelessWidget {
  // 1. Final properties
  final String title;
  final VoidCallback onTap;
  
  // 2. Constructors
  const MyWidget({
    required this.title,
    required this.onTap,
  });
  
  // 3. Build method (for widgets)
  @override
  Widget build(BuildContext context) {
    return Container();
  }
  
  // 4. Helper methods
  void _handleAction() {}
}
```

## 🧪 Testing

### Unit Tests

```dart
// test/models/user_model_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:signverse_ai/models/user_model.dart';

void main() {
  group('UserModel', () {
    test('should parse JSON correctly', () {
      final json = {'id': '1', 'name': 'John'};
      final user = UserModel.fromJson(json);
      
      expect(user.id, '1');
      expect(user.name, 'John');
    });
    
    test('should convert to JSON correctly', () {
      final user = UserModel(id: '1', name: 'John');
      final json = user.toJson();
      
      expect(json['id'], '1');
      expect(json['name'], 'John');
    });
  });
}
```

### Widget Tests

```dart
// test/widgets/sign_widget_test.dart
void main() {
  testWidgets('SignWidget displays sign name', (tester) async {
    const sign = Sign(id: '1', name: 'HELLO');
    
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(body: SignWidget(sign: sign)),
      ),
    );
    
    expect(find.text('HELLO'), findsOneWidget);
  });
}
```

### Running Tests

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/models/user_model_test.dart

# Run with coverage
flutter test --coverage

# View coverage
genhtml coverage/lcov.info -o coverage/html
```

## 🐛 Debugging

### Debug Mode

```bash
# Run in debug mode with verbose logging
flutter run -v

# Attach debugger
flutter attach

# Enable checked mode
flutter run --checked
```

### Print Debugging

```dart
// Basic print
print('Value: $value');

// Debug output
debugPrint('Debug: $value');

// Pretty print
import 'dart:developer';
log('Message', name: 'MyApp');
```

### DevTools

```bash
# Launch DevTools
flutter pub global run devtools

# Open in browser
flutter pub global run devtools -- --port 9100
```

### Common Breakpoint Usage

```dart
// Set breakpoint in VS Code
// Click left margin on line number

// Conditional breakpoint
// Right-click line number > Add Conditional Breakpoint
if (condition) {
  debugBreakpoint(); // Breaks here
}
```

## 📊 Performance Profiling

### CPU Profiling

```bash
# Generate CPU profile
flutter run --profile

# View in DevTools
# Open DevTools > CPU Profiler
```

### Memory Profiling

```bash
# Monitor memory usage
# DevTools > Memory tab

# Take snapshot
# Memory > Take Snapshot

# Analyze heap
# Memory > Export Heap
```

### Widget Rebuild Tracking

```dart
// Enable widget rebuild highlighting
// DevTools > Flutter > Show Widget Rebuilds

// Or in code:
debugPrintBeginFrameBanner = true;
debugPrintEndFrameBanner = true;
```

### Performance Tips

```dart
// ✅ Use const widgets
const MyWidget()

// ✅ Use RepaintBoundary for expensive widgets
RepaintBoundary(child: ExpensiveWidget())

// ✅ Use ListView.builder for long lists
ListView.builder(itemBuilder: ...)

// ✅ Cache images
Image.asset('path', cacheWidth: 200)

// ❌ Avoid setState in build
// ❌ Avoid building complex widgets in build
```

## 🔨 Common Tasks

### Add New Page

```dart
// 1. Create screen
// lib/screens/new_screen.dart
class NewScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(appBar: AppBar(title: Text('New')));
  }
}

// 2. Add route
// lib/routes/app_routes.dart
static const String newPage = '/new';

// 3. Add to route generator
// routes/route_generator.dart
case AppRoutes.newPage:
  return MaterialPageRoute(builder: (_) => const NewScreen());

// 4. Add navigation
// In widget:
context.pushNamed(AppRoutes.newPage);
```

### Add API Endpoint

```dart
// 1. Create model
// lib/models/new_model.dart
class NewModel {
  final String id;
  NewModel({required this.id});
  factory NewModel.fromJson(Map json) => NewModel(id: json['id']);
}

// 2. Add service method
// lib/services/api_service.dart
Future<NewModel> fetchNew() async {
  final response = await _client.get(Uri.parse('$baseUrl/api/new'));
  return NewModel.fromJson(jsonDecode(response.body));
}

// 3. Create provider
// lib/providers/new_provider.dart
final newProvider = FutureProvider((ref) async {
  return await ref.watch(apiServiceProvider).fetchNew();
});

// 4. Use in widget
final newAsync = ref.watch(newProvider);
newAsync.when(
  data: (data) => Text(data.id),
  loading: () => const Loader(),
  error: (err, _) => Text('Error: $err'),
)
```

### Add Camera Feature

```dart
// 1. Add permission
// android/app/src/main/AndroidManifest.xml
<uses-permission android:name="android.permission.CAMERA" />

// ios/Runner/Info.plist
<key>NSCameraUsageDescription</key>
<string>We need camera access for sign recognition</string>

// 2. Request permission
// lib/services/camera_service.dart
import 'package:permission_handler/permission_handler.dart';

Future<bool> requestCameraPermission() async {
  final status = await Permission.camera.request();
  return status.isGranted;
}

// 3. Use camera
final cameras = await availableCameras();
```

### State Management with Provider

```dart
// Define state notifier
class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  
  void increment() => state++;
}

// Define provider
final counterProvider = StateNotifierProvider<CounterNotifier, int>(
  (ref) => CounterNotifier(),
);

// Use in widget
final count = ref.watch(counterProvider);
ref.read(counterProvider.notifier).increment();
```

## 📚 Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)
- [Provider Package](https://pub.dev/packages/provider)
- [Material Design 3](https://m3.material.io/)
- [DevTools Guide](https://flutter.dev/docs/development/tools/devtools)

---

**Last Updated**: December 15, 2025  
**Flutter Version**: 3.13+
