import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  const ApiService({this.baseUrl = 'http://127.0.0.1:8000'});

  Future<Map<String, dynamic>> health() async {
    final response = await http.get(Uri.parse('$baseUrl/api/v1/health'));
    if (response.statusCode != 200) {
      throw Exception('Backend health check failed: ${response.statusCode}');
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> analyze(String symbol) async {
    final response = await http.get(Uri.parse('$baseUrl/api/v1/stocks/$symbol/analyze'));
    if (response.statusCode != 200) {
      throw Exception('Analysis failed: ${response.body}');
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }
}
