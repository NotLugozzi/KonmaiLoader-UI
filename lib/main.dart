import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'resident.dart';
import 'exceed.dart';
import 'vivid.dart';
import 'museca.dart';
import 'package:desktop_webview_window/desktop_webview_window.dart';
import 'dart:io';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:convert';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      routes: {
        '/': (context) => const MyHomePage(),
        '/generalSettings': (context) => const GeneralSettingsPage(),
        '/serverSettings': (context) => const ServerSettings(),
        '/logViewer': (context) =>
            const LogViewer(filePath: 'E:\\KFC-2022122001\\contents\\log.txt'),
        '/shocklinkSettings': (context) => const SLSettingsPage(),
      },
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      darkTheme: ThemeData.dark(),
      themeMode: ThemeMode.system,
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('KonmaiLoaderUi - I:B:F:2023091900'),
      ),
      body: Row(
        children: [
          // Side Panel
          Container(
            width: 314,
            color: const Color(0xFF464650),
            child: ListView(
              padding: const EdgeInsets.symmetric(vertical: 20),
              children: [
                _buildSidePanelItem(context, 'I Miei Giochi', () {
                  // Navigate to the main page (MyHomePage)
                  Navigator.of(context).pushReplacement(
                    MaterialPageRoute(
                      builder: (context) => const MyHomePage(),
                    ),
                  );
                }),
                _buildSidePanelItem(context, 'Impostazioni generali', () {
                  // Navigate to the general settings page
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const GeneralSettingsPage(),
                    ),
                  );
                }),
                _buildSidePanelItem(context, 'Impostazioni Server', () {
                  // Navigate to the general settings page
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const ServerSettings(),
                    ),
                  );
                }),
                _buildSidePanelItem(context, 'Log', () {
                  // Navigate to the general settings page
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const LogViewer(
                          filePath: 'E:\\KFC-2022122001\\contents\\log.txt'),
                    ),
                  );
                }),
                _buildSidePanelItem(context, 'Riconoscimenti', () {
                  // Navigate to the general settings page
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const Credits(),
                    ),
                  );
                }),
                _buildSidePanelItem(context, 'Shocklink Settings', () {
                  // Navigate to the Shocklink settings page
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const SLSettingsPage(),
                    ),
                  );
                }),
              ],
            ),
          ),
          // Main Content
          Expanded(
            child: Container(
              color: const Color(0xFF1B1A1F),
              child: GridView.count(
                crossAxisCount: 3,
                mainAxisSpacing: 11.0,
                crossAxisSpacing: 23.0,
                padding: const EdgeInsets.all(20.0),
                children: [
                  buildGameOption(
                    imagePath: 'lib/assets/resident.png',
                    text:
                        'Beatmania IIDX 30\nLDJ:J:A:A:2023040400\nF:\\LDJ\\003-2023040400\\contents',
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => const ResidentPage(),
                        ),
                      );
                    },
                  ),
                  buildGameOption(
                    imagePath: 'lib/assets/exceed.png',
                    text:
                        'SoundVoltex: Exceed Gear\nKFC:A:G:A:2023091200\nE:\\KFC-003-2023091200\\contents',
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => const ExceedPage(),
                        ),
                      );
                    },
                  ),
                  buildGameOption(
                    imagePath: 'lib/assets/vivid.png',
                    text:
                        'SoundVoltex: vividwave\nKFC:J:F:A:2020122200\nF:\\KFC-008-2020122200\\contents',
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => const VividPage(),
                        ),
                      );
                    },
                  ),
                  buildGameOption(
                    imagePath: 'lib/assets/museca.png',
                    text:
                        'Museca 1+1/2\nPIX:J:B:A:2018073002\nF:\\PIX-2018073002\\contents',
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => const MusecaPage(),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSidePanelItem(
      BuildContext context, String title, VoidCallback onTap) {
    return ListTile(
      title: Text(
        title,
        style:
            const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
      ),
      onTap: onTap,
    );
  }

  Widget buildGameOption({
    required String imagePath,
    required String text,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      child: Container(
        width: 333,
        height: 175,
        decoration: BoxDecoration(
          color: const Color(0xFF4459A8),
          borderRadius: BorderRadius.circular(30),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              imagePath,
              width: 250,
              height: 150,
              fit: BoxFit.contain,
            ),
            const SizedBox(height: 10.0),
            Padding(
              padding: const EdgeInsets.all(5.0),
              child: Text(
                text,
                style: commonTextStyle.copyWith(fontSize: 14.0),
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class SLSettingsPage extends StatefulWidget {
  const SLSettingsPage({super.key});

  @override
  _SLSettingsPageState createState() => _SLSettingsPageState();
}

class _SLSettingsPageState extends State<SLSettingsPage> {
  Map<String, dynamic> _settings = {};

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    try {
      final jsonString =
          await rootBundle.loadString('lib/assets/openshock.json');
      final jsonMap = jsonDecode(jsonString);
      setState(() {
        _settings = jsonMap;
      });
    } catch (e) {
      print('Error loading settings: $e');
    }
  }

  Widget _buildSettingTile(String key, dynamic value) {
    if (value is bool) {
      // Display a checkbox for bool values
      return ListTile(
        title: Text(key),
        trailing: SizedBox(
          width: 50.0, // Adjust the width as needed
          child: Checkbox(
            value: value,
            onChanged: (newValue) {
              setState(() {
                _settings[key] = newValue;
              });
            },
          ),
        ),
      );
    } else {
      return ListTile(
        title: Text(key),
        trailing: SizedBox(
          width: 200.0,
          child: TextFormField(
            initialValue: value.toString(),
            onChanged: (newValue) {
              setState(() {
                _settings[key] = newValue;
              });
            },
          ),
        ),
      );
    }
  }

  Future<void> _saveSettings() async {
    try {
      final settingsJson = jsonEncode(_settings);
      final file = File('lib/assets/openshock.json');
      await file.writeAsString(settingsJson);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Settings saved successfully'),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error saving settings: $e'),
        ),
      );
    }
  }

  Future<void> _clearCachedSettings() async {
    try {
      final jsonString =
          await rootBundle.loadString('lib/assets/openshock.json');
      final jsonMap = jsonDecode(jsonString);
      setState(() {
        _settings = Map.from(jsonMap);
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Cache cleared successfully'),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error clearing cache: $e'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Shocklink Settings'),
      ),
      body: _settings.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _settings.length,
              itemBuilder: (context, index) {
                final key = _settings.keys.elementAt(index);
                final value = _settings[key];
                return _buildSettingTile(key, value);
              },
            ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            ElevatedButton(
              onPressed: _saveSettings,
              child: const Text('Save'),
            ),
            const SizedBox(width: 16.0),
            ElevatedButton(
              onPressed: () {
                _clearCachedSettings();
              },
              child: const Text('Clear Cache'),
            ),
          ],
        ),
      ),
    );
  }
}

class GeneralSettingsPage extends StatefulWidget {
  const GeneralSettingsPage({super.key});

  @override
  _GeneralSettingsPageState createState() => _GeneralSettingsPageState();
}

class _GeneralSettingsPageState extends State<GeneralSettingsPage> {
  Map<String, dynamic> _settings = {};

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    try {
      final jsonString =
          await rootBundle.loadString('lib/assets/generalsettings.json');
      final jsonMap = jsonDecode(jsonString);
      setState(() {
        _settings = jsonMap;
      });
    } catch (e) {
      print('Error loading settings: $e');
    }
  }

  Widget _buildSettingTile(String key, dynamic value) {
    if (value is bool) {
      return ListTile(
        title: Text(key),
        trailing: SizedBox(
          width: 50.0, // Adjust the width as needed
          child: Checkbox(
            value: value,
            onChanged: (newValue) {
              setState(() {
                _settings[key] = newValue;
              });
            },
          ),
        ),
      );
    } else {
      // Display a text input for other types
      return ListTile(
        title: Text(key),
        trailing: SizedBox(
          width: 200.0, // Adjust the width as needed
          child: TextFormField(
            initialValue: value.toString(),
            onChanged: (newValue) {
              setState(() {
                _settings[key] = newValue;
              });
            },
          ),
        ),
      );
    }
  }

  Future<void> _saveSettings() async {
    try {
      final settingsJson = jsonEncode(_settings);
      final file = File('lib/assets/generalsettings.json');
      await file.writeAsString(settingsJson);
// Update cached settings
      // ignore: use_build_context_synchronously
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Settings saved successfully'),
        ),
      );
    } catch (e) {
      // Handle errors while saving settings.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error saving settings: $e'),
        ),
      );
    }
  }

  Future<void> _clearCachedSettings() async {
    try {
      // Reload the JSON file to clear the cache
      final jsonString =
          await rootBundle.loadString('lib/assets/generalsettings.json');
      final jsonMap = jsonDecode(jsonString);
      setState(() {
        _settings = Map.from(jsonMap);
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Cache cleared successfully'),
        ),
      );
    } catch (e) {
      // Handle errors loading the JSON file.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error clearing cache: $e'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Impostazioni Generali'),
      ),
      body: _settings.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _settings.length,
              itemBuilder: (context, index) {
                final key = _settings.keys.elementAt(index);
                final value = _settings[key];
                return _buildSettingTile(key, value);
              },
            ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            ElevatedButton(
              onPressed: _saveSettings,
              child: const Text('Save'),
            ),
            const SizedBox(width: 16.0),
            ElevatedButton(
              onPressed: () {
                _clearCachedSettings();
              },
              child: const Text('Clear Cache'),
            ),
          ],
        ),
      ),
    );
  }
}

class ServerSettings extends StatelessWidget {
  const ServerSettings({super.key});

  void openWebView(BuildContext context) async {
    final webview = await WebviewWindow.create(
      configuration: const CreateConfiguration(
        title: 'Server Options',
        windowWidth: 800,
        windowHeight: 600,
      ),
    );

    webview
      ..setApplicationNameForUserAgent('Mozilla/5.0')
      ..launch(
          ''); // Replace with your server URL
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Server Options'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () => openWebView(context),
          child: const Text('Open Webview'),
        ),
      ),
    );
  }
}

class LocalEA extends StatelessWidget {
  const LocalEA({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Impostazioni Eamuse Locale'),
      ),
      // Add content for the General Settings page
      // ...
    );
  }
}

class DataVerifier extends StatelessWidget {
  const DataVerifier({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Controllo dei file'),
      ),
      // Add content for the General Settings page
      // ...
    );
  }
}

class Patcher extends StatelessWidget {
  const Patcher({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Patcher DLL'),
      ),
      // Add content for the General Settings page
      // ...
    );
  }
}

class LogViewer extends StatelessWidget {
  final String filePath;

  const LogViewer({super.key, required this.filePath});

  Future<String> readFile() async {
    try {
      final file = File(filePath);
      String contents = await file.readAsString();
      return contents;
    } catch (e) {
      return "Error reading file: $e";
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analisi log: KFC:A:G:A:2023091200'),
      ),
      body: FutureBuilder<String>(
        future: readFile(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Text('Error: ${snapshot.error}'),
            );
          } else {
            String fileContent = snapshot.data ?? "";
            return SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(
                  fileContent,
                  style: const TextStyle(
                    fontFamily: 'Consolas',
                    fontSize: 15,
                  ),
                ),
              ),
            );
          }
        },
      ),
    );
  }
}

class Credits extends StatelessWidget {
  const Credits({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Controllo dei file'),
      ),
      body: Center(
        child: ListView(
          children: [
            _buildCenteredText("Frontend UI - GTK4:\nGatsu, Joe.\n\n\n"),
            _buildCenteredText(
                "Frontend - Flutter:\nMercury, ramino, Joe.\n\n\n"),
            _buildCenteredText(
                "Loader - Cpp compat:\nramino, the other Mercury, depa_\n\n\n"),
            _buildCenteredText("Loader - Rust:\nMercury, depa_\n\n\n"),
            _buildCenteredText("LocalEA - porting:\nmid\n\n\n"),
            _buildCenteredText(
                "LocalEA - python server:\nMercury, Gatsu\n\n\n"),
            _buildCenteredText(
                "LocalEA - Score reuploader/netdump:\nMercury\n\n\n"),
            _buildCenteredText("LivePatcher - SDVX:\nGatsu\n\n\n"),
            _buildCenteredText(
                "LivePatcher - IIDX:\nLiterally the whole team worked on this\n(fuck you konmai)\n\n\n"),
            _buildCenteredText("LivePatcher - Other games\ndepa_\n\n\n"),
          ],
        ),
      ),
    );
  }

  Widget _buildCenteredText(String text) {
    return Center(
      child: Text(
        text,
        textAlign: TextAlign.center,
      ),
    );
  }
}
