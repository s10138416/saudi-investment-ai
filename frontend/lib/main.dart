import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const SaudiInvestmentAI());
}

class SaudiInvestmentAI extends StatelessWidget {
  const SaudiInvestmentAI({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Saudi Investment AI',
      theme: ThemeData(useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}
