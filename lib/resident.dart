import 'package:flutter/material.dart';
import 'sidebarwidget.dart'; // Import the sidebar widget

class ResidentPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final logFilePath = 'F:\\LDJ-003-2022103100\\contents\\log.txt'; // Set your desired log file path

    return Scaffold(
      appBar: AppBar(
        title: Text('KonmaiLoader - LDJ:2023090300'),
      ),
      body: Stack(
        children: [
          // Background Image
          Opacity(
            opacity: 0.2, // 60% transparency
            child: Image.asset(
              'lib/assets/resident-hero-small.png',
              fit: BoxFit.cover,
              width: double.infinity,
              height: double.infinity,
            ),
          ),
          Row(
            children: [
              // Include the Sidebar widget here with the logFilePath parameter and showResidentGamingButton
              Sidebar(logFilePath: logFilePath, showResidentGamingButton: true),
              // Main Content
              Expanded(
                child: Container(
                  color: Colors.transparent, // Make the container transparent
                  child: Center(
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
