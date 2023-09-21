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

    // Function to read JSON and truncate values
    Future<String> readAndTruncateJson() async {
      try {
        final String jsonString =
            await DefaultAssetBundle.of(context).loadString(kfcJsonPath);
        final Map<String, dynamic> jsonData = json.decode(jsonString);

        final double totalplaytime = jsonData['total-runtime'];
        final double lastsession = jsonData['last-session'];

        final String truncatedValue1 = totalplaytime.toStringAsFixed(1);
        final String truncatedValue2 = lastsession.toStringAsFixed(1);

        return 'Tempo totale di gioco: $truncatedValue1\nUltima Sessione: $truncatedValue2';
      } catch (e) {
        return 'Error reading JSON data: $e';
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
                  child: FutureBuilder<String>(
                    future: readAndTruncateJson(),
                    builder: (context, snapshot) {
                      if (snapshot.connectionState == ConnectionState.waiting) {
                        return CircularProgressIndicator();
                      } else if (snapshot.hasError) {
                        return Text('Error loading JSON data');
                      } else {
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
                                snapshot.data ?? 'No data available',
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
