import 'package:flutter/material.dart';

class VividPage extends StatelessWidget {
  const VividPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sound Voltex:VividWave'),
      ),
      body: const Center(
        child: Text('We could not find a proper soundvoltex Vividwave installation. check your data or download a newer version.'),
      ),
    );
  }
}
