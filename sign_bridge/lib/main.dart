import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'services/api_client.dart';
import 'services/server_discovery.dart';
import 'screens/home_screen.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const SignVerseApp());
}

class SignVerseApp extends StatelessWidget {
  const SignVerseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<String>(
      // Automatically discover the backend server URL
      future: ServerDiscovery.getServerUrl(),
      builder: (context, snapshot) {
        // Handle discovery states
        if (snapshot.connectionState == ConnectionState.waiting) {
          return MaterialApp(
            title: 'SignVerse AI',
            theme: AppTheme.lightTheme,
            debugShowCheckedModeBanner: false,
            home: Scaffold(
              backgroundColor: AppColors.background,
              body: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Animated loading indicator
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        gradient: AppColors.heroGradient,
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: AppShadows.colored,
                      ),
                      child: const Icon(
                        Icons.sign_language_rounded,
                        color: Colors.white,
                        size: 40,
                      ),
                    ),
                    const SizedBox(height: 24),
                    const CircularProgressIndicator(
                      color: AppColors.primary,
                      strokeWidth: 3,
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'Connecting to server...',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        }

        // Get the server URL (discovered or fallback)
        final serverUrl = snapshot.data ?? 'http://127.0.0.1:8000';

        return Provider<ApiClient>(
          create: (_) => ApiClient(baseUrl: serverUrl),
          child: MaterialApp(
            title: 'SignVerse AI',
            theme: AppTheme.lightTheme,
            debugShowCheckedModeBanner: false,
            home: const HomeScreen(),
          ),
        );
      },
    );
  }
}
