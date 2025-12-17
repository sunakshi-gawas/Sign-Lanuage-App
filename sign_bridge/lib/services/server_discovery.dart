import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:async';

/// Service to automatically discover the backend server on the local network
/// without requiring hardcoded IP addresses.
class ServerDiscovery {
  static const int _connectionTimeout = 1; // seconds per attempt
  static const int _serverPort = 8000;
  
  /// Discovered server base URL (e.g., 'http://192.168.1.100:8000')
  static String? _discoveredUrl;
  
  /// Whether discovery has already been attempted
  static bool _discoveryAttempted = false;

  /// Get the backend server URL, discovering it automatically if needed.
  ///
  /// Returns the discovered or fallback server URL.
  /// Works on any network by scanning the local subnet.
  static Future<String> getServerUrl({
    String fallbackUrl = 'http://127.0.0.1:8000',
  }) async {
    // Return cached discovery result if available
    if (_discoveryAttempted) {
      return _discoveredUrl ?? fallbackUrl;
    }
    
    _discoveryAttempted = true;
    
    try {
      // 1. Get device's own local IP address
      final deviceIp = await _getDeviceLocalIp();
      print('ServerDiscovery: Device IP = $deviceIp');
      
      if (deviceIp != null) {
        // 2. Scan the entire subnet for the server
        print('ServerDiscovery: Scanning subnet for server...');
        final foundUrl = await _scanSubnetForServer(deviceIp);
        if (foundUrl != null) {
          print('ServerDiscovery: ✓ Server found at $foundUrl');
          _discoveredUrl = foundUrl;
          return foundUrl;
        }
        print('ServerDiscovery: ✗ No server found in subnet');
      }
    } catch (e) {
      print('ServerDiscovery: Error during detection: $e');
    }
    
    // Fallback: use localhost or provided fallback
    print('ServerDiscovery: Using fallback URL: $fallbackUrl');
    _discoveredUrl = fallbackUrl;
    return fallbackUrl;
  }

  /// Get the device's local IP address from network interfaces
  static Future<String?> _getDeviceLocalIp() async {
    try {
      // Get the first non-loopback IPv4 address from network interfaces
      final interfaces = await NetworkInterface.list();
      for (final interface in interfaces) {
        print('ServerDiscovery: Checking interface: ${interface.name}');
        for (final addr in interface.addresses) {
          // Look for IPv4 addresses that are not loopback (127.x.x.x)
          if (addr.type == InternetAddressType.IPv4 && !addr.isLoopback) {
            print('ServerDiscovery: Found IPv4 address: ${addr.address}');
            return addr.address;
          }
        }
      }
    } catch (e) {
      print('ServerDiscovery: Error getting device IP: $e');
    }
    return null;
  }

  /// Scan the local subnet for a server by trying IPs in parallel
  static Future<String?> _scanSubnetForServer(String deviceIp) async {
    try {
      // Extract subnet from device IP (e.g., 192.168.65.174 -> 192.168.65)
      final parts = deviceIp.split('.');
      if (parts.length != 4) return null;

      final subnet = '${parts[0]}.${parts[1]}.${parts[2]}';
      final deviceLastOctet = int.tryParse(parts[3]) ?? 0;

      // Prioritize common server IPs - try these first (they're most likely to have the server)
      final priorityIps = <String>[
        '$subnet.10',   // Common for development Mac (172.20.10.10)
        '$subnet.1',    // Often gateway/router, sometimes we run servers here
        '$subnet.2',    // Sometimes router/server
        '$subnet.254',  // Sometimes router
        '$subnet.100',  // Very common for development machines
        '$subnet.50',   // Common for servers
        '$subnet.5',    // Another common IP
        '$subnet.15',   // Another common IP
      ];

      print('ServerDiscovery: Trying priority IPs: $priorityIps');
      
      // Try priority IPs in parallel (fast)
      final priorityResults = await Future.wait(
        priorityIps
            .where((ip) => !ip.endsWith('.$deviceLastOctet'))
            .map((ip) async {
          final url = 'http://$ip:$_serverPort';
          if (await _checkServerAvailable(url)) {
            return url;
          }
          return null;
        }).toList(),
      );
      
      for (final result in priorityResults) {
        if (result != null) return result;
      }

      // Priority IPs didn't work, try full range but with fewer concurrent requests
      print('ServerDiscovery: Priority IPs failed, trying full subnet range...');
      
      final allIps = <String>[];
      for (int i = 1; i <= 254; i++) {
        if (i != deviceLastOctet) {
          final ip = '$subnet.$i';
          if (!priorityIps.contains(ip)) {
            allIps.add(ip);
          }
        }
      }

      // Try in batches of 10 for better parallelism without overwhelming the network
      for (int i = 0; i < allIps.length; i += 10) {
        final batch = allIps.sublist(
          i,
          (i + 10 < allIps.length) ? i + 10 : allIps.length,
        );
        
        final results = await Future.wait(
          batch.map((ip) async {
            final url = 'http://$ip:$_serverPort';
            if (await _checkServerAvailable(url)) {
              return url;
            }
            return null;
          }).toList(),
        );
        
        for (final result in results) {
          if (result != null) return result;
        }
      }
    } catch (e) {
      print('ServerDiscovery: Error scanning subnet: $e');
    }
    return null;
  }

  /// Check if a server is available at the given URL
  static Future<bool> _checkServerAvailable(String url) async {
    try {
      final response = await http
          .get(
            Uri.parse('$url/api/health'),
          )
          .timeout(
            Duration(seconds: _connectionTimeout),
            onTimeout: () => throw TimeoutException('Connection timeout'),
          );

      // Server is available if we get any 2xx response or 404
      // (404 means server is up, but endpoint doesn't exist - still good!)
      final isAvailable = response.statusCode >= 200 && response.statusCode < 500;
      if (isAvailable) {
        // Debug log
        print('✓ Found server at $url (status: ${response.statusCode})');
      }
      return isAvailable;
    } catch (e) {
      // Debug log for errors
      // print('✗ Server check failed for $url: $e');
      return false;
    }
  }

  /// Reset discovery cache (useful for testing or reconnecting)
  static void reset() {
    _discoveredUrl = null;
    _discoveryAttempted = false;
  }

  /// Get the currently discovered URL (or null if not yet discovered)
  static String? getCachedUrl() => _discoveredUrl;

  /// Manually set the server URL (override auto-discovery)
  static void setManualUrl(String url) {
    _discoveredUrl = url;
    _discoveryAttempted = true;
  }
}
