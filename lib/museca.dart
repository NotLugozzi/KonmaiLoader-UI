import 'package:flutter/material.dart';

class MusecaPage extends StatelessWidget {
  const MusecaPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Museca 1+1/2'),
      ),
      body: const Center(
        child: Text('Test Content for Museca settings and patches'),
      ),
    );
  }
}
