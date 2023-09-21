import 'package:flutter/material.dart';
import 'sidebarwidget.dart'; // Import the sidebar widget
import 'dart:convert';

class ExceedPage extends StatelessWidget {
  const ExceedPage({super.key});

  @override
  Widget build(BuildContext context) {
    const logFilePath =
        'F:\\LDJ-003-2022103100\\contents\\log.txt'; // Set your desired log file path
    const kfcJsonPath = 'lib/assets/bin/KFC.json'; // JSON file path

    // Function to read JSON
    Future<Map<String, dynamic>> readJson() async {
      try {
        final String jsonString =
            await DefaultAssetBundle.of(context).loadString(kfcJsonPath);
        final Map<String, dynamic> jsonData = json.decode(jsonString);
        return jsonData;
      } catch (e) {
        return {'error': 'Error reading JSON data: $e'};
      }
    }

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
              const Sidebar(
                  logFilePath: logFilePath, showExceedGamingButton: true),
              // Main Content
              Expanded(
                child: Container(
                  color: Colors.transparent, // Make the container transparent
                  child: FutureBuilder<Map<String, dynamic>>(
                    future: readJson(),
                    builder: (context, snapshot) {
                      if (snapshot.connectionState == ConnectionState.waiting) {
                        return CircularProgressIndicator();
                      } else if (snapshot.hasError) {
                        return Text('Error loading JSON data');
                      } else {
                        final jsonData = snapshot.data;
                        final totalplaytimeStr = jsonData?['total-runtime'];
                        final lastsessionStr = jsonData?['last-session'];

                        return Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                'We are sorry. our team is still working on getting game-specific options and patches - Check back soon for new updates and features!',
                              ),
                              SizedBox(height: 20),
                              Text(
                                'Statistiche Sessione:',
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                              Text(
                                'Tempo totale di gioco: $totalplaytimeStr\nUltima Sessione: $lastsessionStr',
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        );
                      }
                    },
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
