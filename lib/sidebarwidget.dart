import 'package:flutter/material.dart';
import 'dart:io';


class Sidebar extends StatelessWidget {
  final String logFilePath;
  final bool showResidentGamingButton; // Control visibility of Resident Gaming button
  final bool showExceedGamingButton; // Control visibility of Exceed Gaming button

  const Sidebar({super.key, 
    required this.logFilePath,
    this.showResidentGamingButton = false,
    this.showExceedGamingButton = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 314,
      color: const Color(0xFF464650),
      child: ListView(
        padding: const EdgeInsets.symmetric(vertical: 20),
        children: [
          _buildSidePanelItem(context, 'Impostazioni generali', () {
            Navigator.of(context).pushNamed('/generalSettings');
          }),
          _buildSidePanelItem(context, 'Impostazioni Server', () {
            Navigator.of(context).pushNamed('/serverSettings');
          }),
          _buildSidePanelItem(context, 'Log', () {
            Navigator.of(context).pushNamed('/logViewer', arguments: logFilePath);
          }),
          if (showResidentGamingButton)
            _buildSidePanelItem(context, 'Avvia loader-resident.rs', () {
              _launchResidentGamingBat();
            }),
          if (showExceedGamingButton)
            _buildSidePanelItem(context, 'Avvia loader-KFC.rs', () {
              _exceedGear();
            }),
        ],
      ),
    );
  }

  Widget _buildSidePanelItem(BuildContext context, String title, VoidCallback onTap) {
    return ListTile(
      title: Text(
        title,
        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
      ),
      onTap: onTap,
    );
  }

  void _launchResidentGamingBat() async {
    const assetPath = 'lib/assets/bin/residentgaming.bat';

    try {
      final appDir = Directory.current;
      final rustLoader = File('${appDir.path}/$assetPath');

      if (await rustLoader.exists()) {
        final result = await Process.run(rustLoader.path, []);
        print('Result: ${result.stdout}');
      } else {
        print('File not found: $assetPath');
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  void _exceedGear() async {
    const assetPath = 'lib/assets/bin/exceed.bat';

    try {
      final appDir = Directory.current;
      final rustLoader = File('${appDir.path}/$assetPath');

      if (await rustLoader.exists()) {
        final result = await Process.run(rustLoader.path, []);
        print('Result: ${result.stdout}');
      } else {
        print('File not found: $assetPath');
      }
    } catch (e) {
      print('Error: $e');
    }
  }
}