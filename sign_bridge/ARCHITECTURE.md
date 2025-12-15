# Flutter App Architecture

Detailed architecture, design patterns, and code organization for the SignVerse AI Flutter application.

## 📋 Table of Contents

- [Overall Architecture](#overall-architecture)
- [Folder Structure](#folder-structure)
- [Design Patterns](#design-patterns)
- [State Management](#state-management)
- [Navigation](#navigation)
- [Services Layer](#services-layer)
- [Widget Composition](#widget-composition)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)

## 🏗️ Overall Architecture

### Layered Architecture

```
┌────────────────────────────────────────┐
│         Presentation Layer             │
│  Screens, Widgets, UI Components       │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│       Domain Layer (Business Logic)    │
│  Use Cases, Providers, State Notifiers │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│         Data Layer                     │
│  Services (API, Local Storage, etc.)   │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│       External Resources               │
│  Backend API, Device (Camera, TTS)     │
└────────────────────────────────────────┘
```

### Component Interaction

```
User Interaction
       │
       ▼
    Widget (UI)
       │
       ├─── Reads State (Providers)
       │
       ▼
   State Changes
       │
       ├─── Calls Methods on Services
       │
       ▼
   Services (API, Storage, Camera)
       │
       ▼
   External Resources (Backend, Device)
       │
       ▼
   Response → Update State → Rebuild Widget
```

## 📁 Folder Structure

### Detailed Structure

```
lib/
├── main.dart                    # App entry point
│
├── models/                      # Data models
│   ├── sign_model.dart
│   ├── translation_model.dart
│   ├── history_model.dart
│   └── user_settings_model.dart
│
├── providers/                   # State management (Provider)
│   ├── sign_provider.dart
│   ├── translation_provider.dart
│   ├── camera_provider.dart
│   ├── history_provider.dart
│   ├── settings_provider.dart
│   └── app_state_provider.dart
│
├── services/                    # Business logic & API
│   ├── api_service.dart         # Backend API calls
│   ├── ml_service.dart          # ML inference logic
│   ├── camera_service.dart      # Camera management
│   ├── storage_service.dart     # Local storage (SharedPrefs)
│   ├── notification_service.dart # Notifications & alerts
│   └── tts_service.dart         # Text-to-speech
│
├── screens/                     # Full screen pages
│   ├── splash_screen.dart
│   ├── home_screen.dart
│   ├── camera_screen.dart
│   ├── translate_screen.dart
│   ├── history_screen.dart
│   ├── settings_screen.dart
│   └── detail_screen.dart
│
├── widgets/                     # Reusable UI components
│   ├── common/
│   │   ├── app_bar.dart
│   │   ├── bottom_nav_bar.dart
│   │   ├── loading_indicator.dart
│   │   └── error_dialog.dart
│   │
│   ├── sign_widgets/
│   │   ├── sign_display.dart
│   │   ├── sign_animation.dart
│   │   └── confidence_indicator.dart
│   │
│   └── camera_widgets/
│       ├── camera_preview.dart
│       ├── hand_overlay.dart
│       └── gesture_feedback.dart
│
├── routes/                      # Navigation
│   ├── app_routes.dart
│   └── route_generator.dart
│
├── constants/                   # Constants & config
│   ├── api_constants.dart
│   ├── app_constants.dart
│   └── strings.dart
│
├── utils/                       # Utility functions
│   ├── logger.dart
│   ├── validators.dart
│   ├── extensions.dart
│   └── helpers.dart
│
├── theme/                       # Theme & styling
│   ├── app_theme.dart
│   ├── colors.dart
│   └── text_styles.dart
│
└── config/                      # App configuration
    └── config.dart
```

## 🎨 Design Patterns

### 1. Provider Pattern (State Management)

```dart
// Define a simple provider
final counterProvider = StateNotifierProvider<CounterNotifier, int>(
  (ref) => CounterNotifier(),
);

// Define state notifier
class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  
  void increment() => state++;
}

// Use in widget
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

### 2. Service Locator Pattern

```dart
// services/service_locator.dart
import 'package:get_it/get_it.dart';

final getIt = GetIt.instance;

void setupServiceLocator() {
  getIt.registerSingleton<ApiService>(ApiService());
  getIt.registerSingleton<CameraService>(CameraService());
  getIt.registerSingleton<StorageService>(StorageService());
}

// Usage
final apiService = getIt<ApiService>();
```

### 3. Repository Pattern

```dart
// repositories/sign_repository.dart
abstract class SignRepository {
  Future<List<Sign>> getSigns();
  Future<Sign> getSignByName(String name);
}

class SignRepositoryImpl implements SignRepository {
  final ApiService _apiService;
  
  SignRepositoryImpl(this._apiService);
  
  @override
  Future<List<Sign>> getSigns() => _apiService.fetchSigns();
  
  @override
  Future<Sign> getSignByName(String name) => 
    _apiService.fetchSignByName(name);
}
```

### 4. Builder Pattern

```dart
// For complex widgets
class CameraScreenBuilder extends Builder {
  final CameraController controller;
  final Function(XFile) onCapture;
  
  const CameraScreenBuilder({
    required this.controller,
    required this.onCapture,
  });
  
  @override
  Widget build(BuildContext context) {
    return CameraPreview(
      controller,
      child: Overlay(
        initialEntries: [
          OverlayEntry(
            builder: (context) => GestureDetector(
              onTap: () => _captureImage(),
            ),
          ),
        ],
      ),
    );
  }
}
```

## 💾 State Management with Provider

### Provider Types

```dart
// 1. Basic Provider (read-only)
final nameProvider = Provider((ref) => 'SignVerse');

// 2. State Provider (mutable state)
final countProvider = StateProvider<int>((ref) => 0);

// 3. State Notifier Provider (complex state)
final userProvider = StateNotifierProvider<UserNotifier, User>(
  (ref) => UserNotifier(),
);

// 4. Future Provider (async data)
final signsFutureProvider = FutureProvider<List<Sign>>((ref) async {
  return await ref.watch(apiServiceProvider).getSigns();
});

// 5. Async Value Provider
final signsProvider = FutureProvider.autoDispose<List<Sign>>((ref) async {
  return await ref.watch(apiServiceProvider).getSigns();
});

// 6. Family Provider (parameterized)
final signByNameProvider = FutureProvider.family<Sign, String>((ref, name) async {
  return await ref.watch(apiServiceProvider).getSignByName(name);
});
```

### State Notifier Example

```dart
class TranslationNotifier extends StateNotifier<TranslationState> {
  final ApiService _apiService;
  
  TranslationNotifier(this._apiService) 
    : super(TranslationState.initial());
  
  Future<void> translate(String text) async {
    state = state.copyWith(isLoading: true);
    
    try {
      final result = await _apiService.translate(text);
      state = state.copyWith(
        isLoading: false,
        translation: result,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }
}
```

## 🧭 Navigation

### Named Routes

```dart
// routes/app_routes.dart
class AppRoutes {
  static const String home = '/';
  static const String camera = '/camera';
  static const String translate = '/translate';
  static const String history = '/history';
  static const String settings = '/settings';
  static const String signDetail = '/sign-detail';
}

// routes/route_generator.dart
class RouteGenerator {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case AppRoutes.home:
        return MaterialPageRoute(builder: (_) => const HomeScreen());
      case AppRoutes.camera:
        return MaterialPageRoute(builder: (_) => const CameraScreen());
      case AppRoutes.signDetail:
        final args = settings.arguments as String;
        return MaterialPageRoute(
          builder: (_) => SignDetailScreen(signName: args),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => const Scaffold(
            body: Center(child: Text('Route not found')),
          ),
        );
    }
  }
}

// main.dart
MaterialApp(
  onGenerateRoute: RouteGenerator.generateRoute,
  initialRoute: AppRoutes.home,
)
```

### Navigation Usage

```dart
// Navigate to route
context.push(AppRoutes.camera);

// Navigate with arguments
context.pushNamed(AppRoutes.signDetail, arguments: 'HELLO');

// Pop route
context.pop();

// Replace route
context.go(AppRoutes.home);
```

## 🔧 Services Layer

### API Service Pattern

```dart
class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  late final http.Client _client;
  
  ApiService({http.Client? client}) 
    : _client = client ?? http.Client();
  
  Future<List<Sign>> getSigns() async {
    try {
      final response = await _client.get(
        Uri.parse('$baseUrl/api/signs'),
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final json = jsonDecode(response.body);
        return (json['signs'] as List)
          .map((e) => Sign.fromJson(e))
          .toList();
      } else {
        throw HttpException('Failed to load signs');
      }
    } on SocketException {
      throw ConnectionException('No internet connection');
    } catch (e) {
      rethrow;
    }
  }
  
  Future<TranslationResult> translate(String text) async {
    try {
      final response = await _client.post(
        Uri.parse('$baseUrl/api/translate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'text': text, 'language': 'en'}),
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        return TranslationResult.fromJson(jsonDecode(response.body));
      } else {
        throw HttpException('Translation failed');
      }
    } catch (e) {
      rethrow;
    }
  }
}
```

### Camera Service Pattern

```dart
class CameraService {
  late CameraController _controller;
  
  Future<void> initializeCamera() async {
    final cameras = await availableCameras();
    final frontCamera = cameras.firstWhere(
      (c) => c.lensDirection == CameraLensDirection.front,
    );
    
    _controller = CameraController(
      frontCamera,
      ResolutionPreset.high,
      enableAudio: false,
    );
    
    await _controller.initialize();
  }
  
  Future<XFile> captureImage() async {
    return await _controller.takePicture();
  }
  
  Future<void> dispose() async {
    await _controller.dispose();
  }
}
```

## 🎯 Widget Composition

### Stateless Widget Pattern

```dart
class SignDisplayWidget extends StatelessWidget {
  final Sign sign;
  final VoidCallback? onTap;
  
  const SignDisplayWidget({
    required this.sign,
    this.onTap,
  });
  
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        child: Column(
          children: [
            Image.asset(sign.gifPath),
            Text(sign.name),
          ],
        ),
      ),
    );
  }
}
```

### Consumer Widget Pattern

```dart
class TranslationResultWidget extends ConsumerWidget {
  final String text;
  
  const TranslationResultWidget({required this.text});
  
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final translationAsync = ref.watch(translationProvider(text));
    
    return translationAsync.when(
      data: (translation) => Text(translation.result),
      loading: () => const CircularProgressIndicator(),
      error: (error, stack) => Text('Error: $error'),
    );
  }
}
```

## 📊 Data Models

### Model with Serialization

```dart
class Sign {
  final String id;
  final String name;
  final String gifPath;
  final String description;
  
  Sign({
    required this.id,
    required this.name,
    required this.gifPath,
    required this.description,
  });
  
  // JSON serialization
  factory Sign.fromJson(Map<String, dynamic> json) {
    return Sign(
      id: json['id'] as String,
      name: json['name'] as String,
      gifPath: json['gif_path'] as String,
      description: json['description'] as String,
    );
  }
  
  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'gif_path': gifPath,
    'description': description,
  };
  
  // CopyWith for immutability
  Sign copyWith({
    String? id,
    String? name,
    String? gifPath,
    String? description,
  }) {
    return Sign(
      id: id ?? this.id,
      name: name ?? this.name,
      gifPath: gifPath ?? this.gifPath,
      description: description ?? this.description,
    );
  }
}
```

## ⚠️ Error Handling

### Custom Exceptions

```dart
abstract class AppException implements Exception {
  final String message;
  AppException(this.message);
  
  @override
  String toString() => message;
}

class ConnectionException extends AppException {
  ConnectionException(String message) : super(message);
}

class HttpException extends AppException {
  final int statusCode;
  HttpException(this.statusCode, String message) : super(message);
}

class CameraException extends AppException {
  CameraException(String message) : super(message);
}
```

### Error Handling in Widgets

```dart
class SignListWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final signsAsync = ref.watch(signsProvider);
    
    return signsAsync.when(
      data: (signs) => ListView.builder(
        itemCount: signs.length,
        itemBuilder: (context, index) => SignTile(sign: signs[index]),
      ),
      loading: () => const LoadingIndicator(),
      error: (error, stackTrace) => ErrorDialog(
        message: error.toString(),
        onRetry: () => ref.refresh(signsProvider),
      ),
    );
  }
}
```

## ⚡ Performance Optimization

### Image Caching

```dart
final cachedImageProvider = Provider((ref) {
  final imageCache = ImageCache();
  imageCache.maximumSize = 100;
  return imageCache;
});
```

### Lazy Loading

```dart
class SignListWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ListView.builder(
      itemCount: 100,
      itemBuilder: (context, index) {
        // Only load visible items
        return LazyLoadTile(index: index);
      },
    );
  }
}
```

### Memory Management

```dart
class CameraScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends ConsumerState<CameraScreen> {
  @override
  void dispose() {
    // Clean up resources
    ref.read(cameraServiceProvider).dispose();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    // Build widget
  }
}
```

---

**Last Updated**: December 15, 2025  
**Flutter Version**: 3.13+  
**Architecture Pattern**: Layered + Provider Pattern
