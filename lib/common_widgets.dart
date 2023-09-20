import 'package:flutter/material.dart';

// Common Styles
final TextStyle commonTextStyle = TextStyle(
  fontSize: 20,
  fontFamily: 'GoogleSans', // Make sure to load the Google Sans font.
);

// Common Right Side Panel Button
Widget buildCommonButton() {
  return SizedBox(
    height: 76, // Adjusted height
    width: 60,
    child: Container(
      decoration: BoxDecoration(
        color: Color(0xFF412A34),
        borderRadius: BorderRadius.circular(30),
      ),
      child: Center(
        child: Icon(Icons.add, color: Colors.white),
      ),
    ),
  );
}


// Common Page Scaffold
Widget buildCommonPage({
  required String pageTitle,
  required Widget pageContent,
}) {
  return Scaffold(
    appBar: AppBar(
      title: Text(pageTitle),
    ),
    body: pageContent,
  );
}
