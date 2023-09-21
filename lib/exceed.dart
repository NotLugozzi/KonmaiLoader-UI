import 'package:flutter/material.dart';
import 'sidebarwidget.dart'; // Import the sidebar widget

class ExceedPage extends StatelessWidget {
  const ExceedPage({super.key});

  @override
  Widget build(BuildContext context) {
    const logFilePath = 'F:\\LDJ-003-2022103100\\contents\\log.txt'; // Set your desired log file path

    return Scaffold(
      appBar: AppBar(
        title: const Text('KonmaiLoader - KFC:2023091200'),
      ),
      body: Stack(
        children: [
          // Background Image
          Opacity(
            opacity: 0.2, // 20% transparency
            child: Image.asset(
              'lib/assets/exceed-hero.png',
              fit: BoxFit.cover,
              width: double.infinity,
              height: double.infinity,
            ),
          ),
          Row(
            children: [
              // Include the Sidebar widget here with the logFilePath parameter and showExceedGamingButton
              const Sidebar(logFilePath: logFilePath, showExceedGamingButton: true),
              // Main Content
              Expanded(
                child: Container(
                  color: Colors.transparent, // Make the container transparent
                  child: const Center(
                    child: Text('We are sorry. our team is still working on getting game-specific options and patches - Check back soon for new updates and features!'),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
