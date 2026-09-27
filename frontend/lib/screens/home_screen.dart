import 'package:flutter/material.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _symbolController = TextEditingController(text: '2222');
  final _api = const ApiService();
  String _status = 'جاهز';
  bool _loading = false;

  Future<void> _checkBackend() async {
    setState(() => _loading = true);
    try {
      final result = await _api.health();
      setState(() => _status = 'Backend: ${result['status']} | SAHMK: ${result['sahmk_configured']}');
    } catch (e) {
      setState(() => _status = 'خطأ: $e');
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _analyze() async {
    setState(() => _loading = true);
    try {
      final result = await _api.analyze(_symbolController.text.trim());
      setState(() => _status = result.toString());
    } catch (e) {
      setState(() => _status = 'خطأ: $e');
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.rtl,
      child: Scaffold(
        appBar: AppBar(title: const Text('محلل الاستثمار السعودي')),
        body: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text('v0.1.0 — البنية الأساسية', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              TextField(
                controller: _symbolController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'رمز السهم',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 12),
              FilledButton(onPressed: _loading ? null : _analyze, child: const Text('تحليل السهم')),
              const SizedBox(height: 8),
              OutlinedButton(onPressed: _loading ? null : _checkBackend, child: const Text('فحص الاتصال')),
              const SizedBox(height: 20),
              if (_loading) const LinearProgressIndicator(),
              const SizedBox(height: 12),
              Expanded(child: SingleChildScrollView(child: SelectableText(_status))),
            ],
          ),
        ),
      ),
    );
  }
}
