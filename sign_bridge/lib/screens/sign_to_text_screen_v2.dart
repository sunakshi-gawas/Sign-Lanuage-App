import 'dart:async';
import 'dart:typed_data';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:provider/provider.dart';

import '../services/api_client.dart';
import '../theme/app_theme.dart';

class SignToTextScreenV2 extends StatefulWidget {
  const SignToTextScreenV2({super.key});

  @override
  State<SignToTextScreenV2> createState() => _SignToTextScreenV2State();
}

class _SignToTextScreenV2State extends State<SignToTextScreenV2> {
  CameraController? _cameraController;

  String _statusText = 'Point your hand at the camera.';
  bool _isDetecting = false;
  bool _isRealTimeActive = false;
  Timer? _detectionTimer;

  late final FlutterTts _flutterTts;

  // Language support: English, Hindi, Marathi
  String _selectedLanguage = 'en-US';
  final Map<String, String> _languages = {
    'en-US': 'English',
    'mr-IN': 'Marathi',
  };

  // Advanced speech features
  double _speechSpeed = 0.9; // Default speech rate (0.5 - 2.0)
  String _selectedVoice = 'default'; // Voice selection
  List<Map<String, dynamic>> _detectionHistory =
      []; // Stores {text, confidence, timestamp}
  Timer? _speedDebounce;

  // Voice options
  final Map<String, String> _voiceOptions = {
    'default': 'Default Voice',
    'slow': 'Slow & Clear',
    'fast': 'Fast',
    'high': 'High Pitch',
  };

  @override
  void initState() {
    super.initState();
    _flutterTts = FlutterTts();
    _setupTts();
    _initCameraSystem();
  }

  Future<void> _setupTts() async {
    await _flutterTts.setLanguage(_selectedLanguage);
    await _flutterTts.setPitch(_getPitchFromVoice());
    await _flutterTts.setSpeechRate(_speechSpeed);
  }

  double _getPitchFromVoice() {
    switch (_selectedVoice) {
      case 'high':
        return 1.5;
      default:
        return 1.0;
    }
  }

  double _getSpeedFromVoice() {
    switch (_selectedVoice) {
      case 'slow':
        return 0.5;
      case 'fast':
        return 1.5;
      default:
        return _speechSpeed;
    }
  }

  Future<void> _changeLanguage(String newLanguage) async {
    setState(() {
      _selectedLanguage = newLanguage;
    });
    // Fire-and-forget to avoid blocking UI
    _flutterTts.setLanguage(newLanguage);
  }

  Future<void> _changeVoice(String newVoice) async {
    setState(() {
      _selectedVoice = newVoice;
    });
    // Apply voice tweaks without awaiting to keep UI responsive
    _flutterTts.setPitch(_getPitchFromVoice());
    _flutterTts.setSpeechRate(_getSpeedFromVoice());
  }

  Future<void> _changeSpeed(double newSpeed) async {
    setState(() {
      _speechSpeed = newSpeed;
    });
    // Debounce rapid slider updates to avoid jank
    if (_speedDebounce?.isActive ?? false) {
      _speedDebounce!.cancel();
    }
    _speedDebounce = Timer(const Duration(milliseconds: 200), () {
      _flutterTts.setSpeechRate(_speechSpeed);
    });
  }

  Future<void> _speak(String text, {bool addToHistory = true}) async {
    if (text.isEmpty) return;
    if (text.startsWith('Camera ') ||
        text.startsWith('Error:') ||
        text.startsWith('No hand detected') ||
        text.startsWith('Sign recognition error')) {
      return;
    }

    await _flutterTts.stop();
    await _flutterTts.speak(text);
  }

  // Store only front and back camera (not all lenses)
  CameraDescription? _frontCamera;
  CameraDescription? _backCamera;
  bool _isFrontCamera = true;

  Future<void> _initCameraSystem() async {
    try {
      final allCameras = await availableCameras();

      if (allCameras.isEmpty) {
        setState(() {
          _statusText = 'No camera available on this device.';
        });
        return;
      }

      // Find the FIRST front camera and FIRST back camera only
      for (final camera in allCameras) {
        if (camera.lensDirection == CameraLensDirection.front &&
            _frontCamera == null) {
          _frontCamera = camera;
          print('[DEBUG] Found front camera: ${camera.name}');
        } else if (camera.lensDirection == CameraLensDirection.back &&
            _backCamera == null) {
          _backCamera = camera;
          print('[DEBUG] Found back camera: ${camera.name}');
        }
      }

      print('[DEBUG] Total cameras found: ${allCameras.length}');
      print(
        '[DEBUG] Using front: ${_frontCamera?.name}, back: ${_backCamera?.name}',
      );

      // Start with front camera if available, otherwise back
      if (_frontCamera != null) {
        _isFrontCamera = true;
        await _setupCameraWithDescription(_frontCamera!);
      } else if (_backCamera != null) {
        _isFrontCamera = false;
        await _setupCameraWithDescription(_backCamera!);
      } else {
        setState(() {
          _statusText = 'No usable camera found.';
        });
      }
    } catch (e) {
      setState(() {
        _statusText = 'Camera init error: $e';
      });
    }
  }

  bool _isSwitchingCamera = false;
  int _cameraKey = 0; // Used to force rebuild

  Future<void> _setupCameraWithDescription(CameraDescription camera) async {
    final controller = CameraController(
      camera,
      ResolutionPreset.medium,
      enableAudio: false,
    );

    try {
      await controller.initialize();

      if (mounted) {
        setState(() {
          _cameraController = controller;
          _cameraKey++; // Force widget rebuild
        });
      }
    } catch (e) {
      print('[DEBUG] Camera init error: $e');
      rethrow;
    }
  }

  Future<void> _disposeCamera() async {
    final controller = _cameraController;
    _cameraController = null;

    if (controller != null) {
      try {
        await controller.dispose();
      } catch (e) {
        print('[DEBUG] Camera dispose error: $e');
      }
    }
  }

  bool get _canFlipCamera => _frontCamera != null && _backCamera != null;

  void _onFlipCameraPressed() async {
    // Guard against multiple taps
    if (!_canFlipCamera) return;
    if (_isSwitchingCamera) return;

    print('[DEBUG] Flip camera pressed');

    // Stop detection if running
    final wasDetecting = _isRealTimeActive;
    if (_isRealTimeActive) {
      _detectionTimer?.cancel();
      _detectionTimer = null;
      _isRealTimeActive = false;
    }

    // Set switching state
    if (mounted) {
      setState(() {
        _isSwitchingCamera = true;
        _statusText = 'Switching camera...';
      });
    }

    // Dispose current camera
    await _disposeCamera();

    // Wait for disposal to complete
    await Future.delayed(const Duration(milliseconds: 200));

    // Toggle between front and back camera
    _isFrontCamera = !_isFrontCamera;

    // Get the target camera
    CameraDescription? targetCamera;
    if (_isFrontCamera && _frontCamera != null) {
      targetCamera = _frontCamera;
    } else if (!_isFrontCamera && _backCamera != null) {
      targetCamera = _backCamera;
    } else {
      // Fallback to the other camera if one is not available
      targetCamera = _isFrontCamera ? _backCamera : _frontCamera;
      _isFrontCamera = !_isFrontCamera;
    }

    if (targetCamera == null) {
      setState(() {
        _isSwitchingCamera = false;
        _statusText = 'No camera available to switch.';
      });
      return;
    }

    print('[DEBUG] Switching to ${_isFrontCamera ? "FRONT" : "BACK"} camera');

    try {
      // Setup new camera
      await _setupCameraWithDescription(targetCamera);

      print('[DEBUG] Camera setup complete');

      if (mounted) {
        setState(() {
          _isSwitchingCamera = false;
          _statusText = 'Camera ready.';
        });
      }

      // Resume detection if it was active
      if (wasDetecting && mounted) {
        await Future.delayed(const Duration(milliseconds: 300));
        _startRealTimeDetection();
      }
    } catch (e) {
      print('[DEBUG] Camera switch failed: $e');
      if (mounted) {
        setState(() {
          _isSwitchingCamera = false;
          _statusText = 'Camera error. Try again.';
        });
      }
    }
  }

  /// Start continuous real-time sign detection
  void _startRealTimeDetection() async {
    final controller = _cameraController;
    if (controller == null || !controller.value.isInitialized) {
      setState(() {
        _statusText = 'Camera is not ready yet.';
      });
      return;
    }

    if (_isRealTimeActive) {
      _stopRealTimeDetection();
      return;
    }

    // Get API client once before starting the timer
    final api = context.read<ApiClient>();

    setState(() {
      _isRealTimeActive = true;
      _statusText = 'Real-time detection active...';
      _detectionHistory = [];
    });

    // Capture frames every 500ms (2 fps)
    _detectionTimer = Timer.periodic(Duration(milliseconds: 500), (_) async {
      if (!_isRealTimeActive || _isDetecting) return;

      // Check if controller is still valid
      if (!controller.value.isInitialized) {
        print('[WARNING] Camera controller not valid, stopping detection');
        _stopRealTimeDetection();
        return;
      }

      try {
        setState(() {
          _isDetecting = true;
        });

        final XFile file = await controller.takePicture();
        final Uint8List bytes = await file.readAsBytes();

        String langCode = _selectedLanguage.split('-').first;

        try {
          final response = await api.signToTextFromImage(
            bytes,
            language: langCode,
          );

          final String text = response['text'] ?? 'Unknown';
          final double confidence = (response['confidence'] ?? 0.0).toDouble();

          print(
            '[DEBUG] Detection: $text (confidence: ${confidence.toStringAsFixed(3)})',
          );

          // Only update if it's a valid detection (confidence > 0.15 threshold)
          if (!text.startsWith('Error:') &&
              !text.startsWith('No hand detected') &&
              text.isNotEmpty &&
              confidence > 0.15) {
            setState(() {
              // Add to detection history if text changed significantly
              if (_detectionHistory.isEmpty ||
                  _detectionHistory.last['text'] != text) {
                _detectionHistory.add({
                  'text': text,
                  'confidence': confidence,
                  'timestamp': DateTime.now(),
                });
                final signList = _detectionHistory
                    .map(
                      (d) =>
                          '${d['text']} (${(d['confidence'] * 100).toStringAsFixed(0)}%)',
                    )
                    .join(' → ');
                _statusText = 'Detected: $signList';
                print('[DEBUG] Updated status: $_statusText');
              }
            });

            // Speak the newly detected sign
            await _speak(text);
          }
        } catch (apiError) {
          print('[ERROR] API call failed: $apiError');
          setState(() {
            _statusText = 'API Error: $apiError';
          });
        }
      } catch (e) {
        // Silently ignore frame capture errors during real-time mode
        print('[DEBUG] Frame capture error: $e');
      } finally {
        setState(() {
          _isDetecting = false;
        });
      }
    });
  }

  void _stopRealTimeDetection() {
    _detectionTimer?.cancel();
    _detectionTimer = null;
    setState(() {
      _isRealTimeActive = false;
      if (_detectionHistory.isNotEmpty) {
        final signList = _detectionHistory
            .map(
              (d) =>
                  '${d['text']} (${(d['confidence'] * 100).toStringAsFixed(0)}%)',
            )
            .join(' → ');
        _statusText = 'Detected: $signList';
      } else {
        _statusText = 'Real-time detection stopped.';
      }
    });
  }

  /// Clear detected signs
  void _clearHistory() {
    setState(() {
      _detectionHistory = [];
      _statusText = 'History cleared.';
    });
  }

  /// Replay last detected signs
  void _replayLastSigns() async {
    if (_detectionHistory.isEmpty) {
      setState(() {
        _statusText = 'No signs detected yet.';
      });
      return;
    }

    final signList = _detectionHistory
        .map(
          (d) =>
              '${d['text']} (${(d['confidence'] * 100).toStringAsFixed(0)}%)',
        )
        .join(' → ');
    setState(() {
      _statusText = 'Replaying: $signList';
    });

    for (final detection in _detectionHistory) {
      await _speak(detection['text'], addToHistory: false);
      await Future.delayed(Duration(milliseconds: 500));
    }
  }

  /// Show settings dialog
  void _showSettingsDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(
          builder: (context, setState) {
            return AlertDialog(
              backgroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
              title: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFF7C3AED), Color(0xFF8B5CF6)],
                      ),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(
                      Icons.tune_rounded,
                      color: Colors.white,
                      size: 20,
                    ),
                  ),
                  const SizedBox(width: 12),
                  const Text(
                    'Settings',
                    style: TextStyle(fontWeight: FontWeight.w700, fontSize: 20),
                  ),
                ],
              ),
              content: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Language selector
                    const Text(
                      'Language',
                      style: TextStyle(
                        fontWeight: FontWeight.w600,
                        fontSize: 14,
                        color: Color(0xFF374151),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Container(
                      decoration: BoxDecoration(
                        border: Border.all(color: const Color(0xFFE5E7EB)),
                        borderRadius: BorderRadius.circular(12),
                        color: const Color(0xFFF9FAFB),
                      ),
                      child: DropdownButton<String>(
                        value: _selectedLanguage,
                        isExpanded: true,
                        underline: const SizedBox(),
                        icon: const Icon(
                          Icons.keyboard_arrow_down_rounded,
                          color: Color(0xFF7C3AED),
                        ),
                        items: _languages.entries
                            .map(
                              (entry) => DropdownMenuItem(
                                value: entry.key,
                                child: Padding(
                                  padding: const EdgeInsets.all(12),
                                  child: Text(entry.value),
                                ),
                              ),
                            )
                            .toList(),
                        onChanged: (newValue) {
                          if (newValue != null) {
                            _changeLanguage(newValue);
                            // Refresh only the dialog UI to avoid rebuilding camera preview
                            setState(() {});
                          }
                        },
                      ),
                    ),
                    const SizedBox(height: 18),
                    // Voice selector
                    const Text(
                      'Voice Style',
                      style: TextStyle(
                        fontWeight: FontWeight.w600,
                        fontSize: 14,
                        color: Color(0xFF374151),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Container(
                      decoration: BoxDecoration(
                        border: Border.all(color: const Color(0xFFE5E7EB)),
                        borderRadius: BorderRadius.circular(12),
                        color: const Color(0xFFF9FAFB),
                      ),
                      child: DropdownButton<String>(
                        value: _selectedVoice,
                        isExpanded: true,
                        underline: const SizedBox(),
                        items: _voiceOptions.entries
                            .map(
                              (entry) => DropdownMenuItem(
                                value: entry.key,
                                child: Padding(
                                  padding: const EdgeInsets.all(8),
                                  child: Text(entry.value),
                                ),
                              ),
                            )
                            .toList(),
                        onChanged: (newValue) {
                          if (newValue != null) {
                            _changeVoice(newValue);
                            // Refresh only the dialog UI to avoid rebuilding camera preview
                            setState(() {});
                          }
                        },
                      ),
                    ),
                    const SizedBox(height: 18),
                    // Speech speed slider
                    const Text(
                      'Speech Speed',
                      style: TextStyle(
                        fontWeight: FontWeight.w600,
                        fontSize: 14,
                        color: Color(0xFF374151),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 8,
                      ),
                      decoration: BoxDecoration(
                        border: Border.all(color: const Color(0xFFE5E7EB)),
                        borderRadius: BorderRadius.circular(12),
                        color: const Color(0xFFF9FAFB),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 10,
                              vertical: 4,
                            ),
                            decoration: BoxDecoration(
                              color: const Color(0xFF7C3AED).withOpacity(0.1),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              '${_speechSpeed.toStringAsFixed(1)}x',
                              style: const TextStyle(
                                fontWeight: FontWeight.w600,
                                color: Color(0xFF7C3AED),
                              ),
                            ),
                          ),
                          Expanded(
                            child: Slider(
                              value: _speechSpeed,
                              min: 0.5,
                              max: 2.0,
                              divisions: 15,
                              activeColor: const Color(0xFF7C3AED),
                              inactiveColor: const Color(0xFFE5E7EB),
                              onChanged: (value) {
                                _changeSpeed(value);
                                // Refresh only the dialog UI while sliding
                                setState(() {});
                              },
                              onChangeEnd: (_) {
                                // Flush pending debounced update
                                _flutterTts.setSpeechRate(_speechSpeed);
                              },
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text(
                    'Close',
                    style: TextStyle(
                      color: Color(0xFF7C3AED),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            );
          },
        );
      },
    );
  }

  @override
  void dispose() {
    _detectionTimer?.cancel();
    _cameraController?.dispose();
    _speedDebounce?.cancel();
    _flutterTts.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final controller = _cameraController;
    // final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        elevation: 0,
        flexibleSpace: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF7C3AED), Color(0xFF8B5CF6)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
        ),
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.2),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(
                Icons.front_hand_rounded,
                size: 20,
                color: Colors.white,
              ),
            ),
            const SizedBox(width: 10),
            const Text(
              'Sign to Text',
              style: TextStyle(
                fontWeight: FontWeight.w700,
                fontSize: 18,
                color: Colors.white,
              ),
            ),
          ],
        ),
        backgroundColor: Colors.transparent,
        iconTheme: const IconThemeData(color: Colors.white),
        actions: [
          Container(
            margin: const EdgeInsets.only(right: 8),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.15),
              borderRadius: BorderRadius.circular(10),
            ),
            child: IconButton(
              onPressed: _showSettingsDialog,
              icon: const Icon(Icons.tune_rounded, size: 22),
              tooltip: 'Settings',
            ),
          ),
        ],
      ),
      body: _buildBody(controller),
    );
  }

  Widget _buildBody(CameraController? controller) {
    // Show loading while switching camera
    if (_isSwitchingCamera) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(
              color: Color(0xFF7C3AED),
              strokeWidth: 3,
            ),
            const SizedBox(height: 16),
            Text(
              'Switching camera...',
              style: TextStyle(color: AppColors.textSecondary, fontSize: 14),
            ),
          ],
        ),
      );
    }

    // Show message if no camera
    if (controller == null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.camera_alt_outlined,
              size: 64,
              color: AppColors.textMuted,
            ),
            const SizedBox(height: 16),
            Text(
              _statusText,
              style: TextStyle(color: AppColors.textSecondary, fontSize: 14),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      );
    }

    // Show loading while camera initializes
    if (!controller.value.isInitialized) {
      return const Center(
        child: CircularProgressIndicator(
          color: Color(0xFF7C3AED),
          strokeWidth: 3,
        ),
      );
    }

    // Show camera preview
    return SingleChildScrollView(
      child: Column(
        children: [
          // Camera preview with gradient border and flip button
          Stack(
            children: [
              Container(
                margin: const EdgeInsets.only(
                  top: 20.0,
                  left: 16.0,
                  right: 16.0,
                ),
                padding: const EdgeInsets.all(3),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(24),
                  gradient: const LinearGradient(
                    colors: [Color(0xFF7C3AED), Color(0xFFF97316)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF7C3AED).withOpacity(0.3),
                      blurRadius: 20,
                      offset: const Offset(0, 8),
                    ),
                  ],
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(21),
                  child: SizedBox(
                    height: MediaQuery.of(context).size.height * 0.45,
                    width: double.infinity,
                    child: FittedBox(
                      fit: BoxFit.cover,
                      clipBehavior: Clip.hardEdge,
                      child: SizedBox(
                        width: controller.value.previewSize?.height ?? 1,
                        height: controller.value.previewSize?.width ?? 1,
                        child: CameraPreview(
                          key: ValueKey('camera_$_cameraKey'),
                          controller,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              // Flip camera button overlay
              if (_canFlipCamera)
                Positioned(
                  top: 32,
                  right: 28,
                  child: GestureDetector(
                    onTap: _isSwitchingCamera ? null : _onFlipCameraPressed,
                    child: Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.5),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: _isSwitchingCamera
                          ? const SizedBox(
                              width: 24,
                              height: 24,
                              child: CircularProgressIndicator(
                                color: Colors.white,
                                strokeWidth: 2,
                              ),
                            )
                          : const Icon(
                              Icons.flip_camera_ios_rounded,
                              color: Colors.white,
                              size: 24,
                            ),
                    ),
                  ),
                ),
            ],
          ),

          const SizedBox(height: 16),

          // Detection status card
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: _isRealTimeActive
                      ? const Color(0xFF22C55E).withOpacity(0.3)
                      : AppColors.border,
                  width: 1.5,
                ),
                boxShadow: [
                  BoxShadow(
                    color: _isRealTimeActive
                        ? const Color(0xFF22C55E).withOpacity(0.1)
                        : Colors.black.withOpacity(0.05),
                    blurRadius: 16,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            gradient: _isRealTimeActive
                                ? const LinearGradient(
                                    colors: [
                                      Color(0xFF22C55E),
                                      Color(0xFF16A34A),
                                    ],
                                  )
                                : const LinearGradient(
                                    colors: [
                                      Color(0xFF8B5CF6),
                                      Color(0xFF7C3AED),
                                    ],
                                  ),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Icon(
                            _isRealTimeActive
                                ? Icons.sensors_rounded
                                : Icons.touch_app_rounded,
                            color: Colors.white,
                            size: 22,
                          ),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                _isRealTimeActive
                                    ? 'Detection Active'
                                    : 'Ready to Detect',
                                style: TextStyle(
                                  fontWeight: FontWeight.w700,
                                  fontSize: 16,
                                  color: _isRealTimeActive
                                      ? const Color(0xFF16A34A)
                                      : AppColors.textPrimary,
                                ),
                              ),
                              const SizedBox(height: 2),
                              if (_detectionHistory.isNotEmpty)
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 8,
                                    vertical: 3,
                                  ),
                                  decoration: BoxDecoration(
                                    color: const Color(
                                      0xFFF97316,
                                    ).withOpacity(0.1),
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Text(
                                    '${_detectionHistory.length} sign(s) detected',
                                    style: const TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w600,
                                      color: Color(0xFFEA580C),
                                    ),
                                  ),
                                )
                              else
                                Text(
                                  'Point your hand at the camera',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: AppColors.textSecondary,
                                  ),
                                ),
                            ],
                          ),
                        ),
                        if (_isRealTimeActive)
                          Container(
                            width: 12,
                            height: 12,
                            decoration: BoxDecoration(
                              color: const Color(0xFF22C55E),
                              shape: BoxShape.circle,
                              boxShadow: [
                                BoxShadow(
                                  color: const Color(
                                    0xFF22C55E,
                                  ).withOpacity(0.5),
                                  blurRadius: 8,
                                ),
                              ],
                            ),
                          ),
                      ],
                    ),
                    const SizedBox(height: 14),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: AppColors.surface,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        _statusText,
                        style: TextStyle(
                          fontSize: 14,
                          color: AppColors.textSecondary,
                          height: 1.5,
                        ),
                        maxLines: 3,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          const SizedBox(height: 16),

          // Control buttons
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Main detection button
                Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    gradient: _isRealTimeActive
                        ? const LinearGradient(
                            colors: [Color(0xFFEF4444), Color(0xFFDC2626)],
                          )
                        : const LinearGradient(
                            colors: [Color(0xFF22C55E), Color(0xFF16A34A)],
                          ),
                    boxShadow: [
                      BoxShadow(
                        color: _isRealTimeActive
                            ? const Color(0xFFEF4444).withOpacity(0.4)
                            : const Color(0xFF22C55E).withOpacity(0.4),
                        blurRadius: 12,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: ElevatedButton(
                    onPressed: _isRealTimeActive
                        ? _stopRealTimeDetection
                        : _startRealTimeDetection,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.transparent,
                      shadowColor: Colors.transparent,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          _isRealTimeActive
                              ? Icons.stop_circle_rounded
                              : Icons.play_circle_rounded,
                          size: 26,
                        ),
                        const SizedBox(width: 10),
                        Text(
                          _isRealTimeActive
                              ? 'Stop Detection'
                              : 'Start Detection',
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 14),
                // Secondary buttons
                Row(
                  children: [
                    Expanded(
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(14),
                          color: _detectionHistory.isEmpty
                              ? AppColors.surface
                              : const Color(0xFF7C3AED).withOpacity(0.1),
                          border: Border.all(
                            color: _detectionHistory.isEmpty
                                ? AppColors.border
                                : const Color(0xFF7C3AED).withOpacity(0.3),
                          ),
                        ),
                        child: TextButton.icon(
                          onPressed: _detectionHistory.isEmpty
                              ? null
                              : _replayLastSigns,
                          icon: Icon(
                            Icons.replay_rounded,
                            size: 20,
                            color: _detectionHistory.isEmpty
                                ? AppColors.textDisabled
                                : const Color(0xFF7C3AED),
                          ),
                          label: Text(
                            'Replay',
                            style: TextStyle(
                              fontWeight: FontWeight.w600,
                              color: _detectionHistory.isEmpty
                                  ? AppColors.textDisabled
                                  : const Color(0xFF7C3AED),
                            ),
                          ),
                          style: TextButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(14),
                          color: _detectionHistory.isEmpty
                              ? AppColors.surface
                              : const Color(0xFFF97316).withOpacity(0.1),
                          border: Border.all(
                            color: _detectionHistory.isEmpty
                                ? AppColors.border
                                : const Color(0xFFF97316).withOpacity(0.3),
                          ),
                        ),
                        child: TextButton.icon(
                          onPressed: _detectionHistory.isEmpty
                              ? null
                              : _clearHistory,
                          icon: Icon(
                            Icons.delete_outline_rounded,
                            size: 20,
                            color: _detectionHistory.isEmpty
                                ? AppColors.textDisabled
                                : const Color(0xFFF97316),
                          ),
                          label: Text(
                            'Clear',
                            style: TextStyle(
                              fontWeight: FontWeight.w600,
                              color: _detectionHistory.isEmpty
                                  ? AppColors.textDisabled
                                  : const Color(0xFFF97316),
                            ),
                          ),
                          style: TextButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          const SizedBox(height: 24),
        ],
      ),
    );
  }
}
