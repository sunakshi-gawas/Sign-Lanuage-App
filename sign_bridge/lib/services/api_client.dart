import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;

class ApiClient {
  final String baseUrl;

  ApiClient({required this.baseUrl});

  static const Map<String, String> _jsonHeaders = {
    'Content-Type': 'application/json',
  };

  /// SIGN → TEXT (feature vector – if you ever use it)
  Future<String> signToText(List<double> features) async {
    final uri = Uri.parse('$baseUrl/api/sign-to-text');

    final res = await http
        .post(
          uri,
          headers: _jsonHeaders,
          body: jsonEncode({'features': features}),
        )
        .timeout(const Duration(seconds: 8));

    if (res.statusCode != 200) {
      throw Exception(_parseError(res));
    }

    return _readTextFromBody(res.body);
  }

  /// SIGN → TEXT (camera image) - Returns text and confidence score
  Future<Map<String, dynamic>> signToTextFromImage(
    Uint8List imageBytes, {
    String language = 'en',
  }) async {
    final uri = Uri.parse(
      '$baseUrl/api/sign-to-text-image?language=$language',
    );

    final res = await http
        .post(
          uri,
          headers: {'Content-Type': 'application/octet-stream'},
          body: imageBytes,
        )
        .timeout(const Duration(seconds: 8));

    if (res.statusCode != 200) {
      throw Exception(_parseError(res));
    }

    try {
      final decoded = jsonDecode(res.body);
      if (decoded is Map<String, dynamic>) {
        return {
          'text': decoded['text'] ?? 'Unknown',
          'confidence': decoded['confidence'] ?? 0.0,
        };
      }
      throw Exception('Invalid response format');
    } catch (_) {
      throw Exception('Invalid JSON from backend: ${res.body}');
    }
  }

  /// TEXT → SIGN (dynamic GIFs)
  ///
  /// Backend returns:
  /// {
  ///   "sign_tokens": ["HELLO", "PLEASE", "HELP"],
  ///   "avatar_animation_ids": ["/sign_gifs/HELLO.gif", ...]
  /// }
  Future<Map<String, dynamic>> textToSign(
    String text,
    String signLanguage,
  ) async {
    final uri = Uri.parse('$baseUrl/api/text-to-sign');

    final res = await http
        .post(
          uri,
          headers: _jsonHeaders,
          body: jsonEncode({
            'text': text,
            'sign_language': signLanguage,
          }),
        )
        .timeout(const Duration(seconds: 12));

    if (res.statusCode != 200) {
      throw Exception(_parseError(res));
    }

    final decoded = jsonDecode(res.body);
    if (decoded is! Map<String, dynamic>) {
      throw Exception('Invalid JSON from backend.');
    }
    return decoded;
  }

  // ================== helpers ==================

  String _readTextFromBody(String body) {
    try {
      final decoded = jsonDecode(body);
      if (decoded is Map && decoded['text'] is String) {
        return decoded['text'] as String;
      }
      throw Exception('Response missing "text" field.');
    } catch (_) {
      throw Exception('Invalid JSON from backend: $body');
    }
  }

  String _parseError(http.Response res) {
    try {
      final decoded = jsonDecode(res.body);
      if (decoded is Map && decoded['detail'] is String) {
        return decoded['detail'] as String;
      }
      return 'Backend error ${res.statusCode}: ${res.body}';
    } catch (_) {
      return 'Backend error ${res.statusCode}: ${res.body}';
    }
  }
}
