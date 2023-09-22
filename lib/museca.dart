import 'package:flutter/material.dart';
import 'sidebarwidget.dart'; // Import the sidebar widget
import 'dart:convert';

class MusecaPage extends StatelessWidget {
  const MusecaPage({super.key});

  @override
  Widget build(BuildContext context) {
    const logFilePath =
        'F:\\LDJ-003-2022103100\\contents\\log.txt'; // Set your desired log file path
    const kfcJsonPath = 'lib/assets/bin/PIX.json'; // JSON file path

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
        title: const Text('KonmaiLoader - PIX:2018073002'),
      ),
      body: Stack(
        children: [
          // Background Image
          Opacity(
            opacity: 0.2, // 20% transparency
            child: Image.asset(
              'lib/assets/museca-background.png',
              fit: BoxFit.cover,
              width: double.infinity,
              height: double.infinity,
            ),
          ),
          Row(
            children: [
              // Include the Sidebar widget here with the logFilePath parameter and showResidentGamingButton
              const Sidebar(
                  logFilePath: logFilePath, showMusecaLauncher: true),
              // Main Content
              Expanded(
                child: Container(
                  color: Colors.transparent, // Make the container transparent
                  child: FutureBuilder<Map<String, dynamic>>(
                    future: readJson(),
                    builder: (context, snapshot) {
                      if (snapshot.connectionState == ConnectionState.waiting) {
                        return const CircularProgressIndicator();
                      } else if (snapshot.hasError) {
                        return const Text('Error loading JSON data');
                      } else {
                        final jsonData = snapshot.data;
                        final totalplaytime = jsonData?['total-runtime'];
                        final lastsession = jsonData?['last-session'];

                        return Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text(
                                'There are no available options for this spec code',
                              ),
                              const SizedBox(height: 20),
                              const Text(
                                'Statistiche Sessione:',
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                              Text(
                                'Tempo totale di gioco: $totalplaytime\nUltima Sessione: $lastsession',
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