import 'dart:convert';

import 'package:http/http.dart' as http;

import 'apiconfig.dart';


class API {
  static Future<String> getBaseUrl() async {
    final config = await APIConfigLoader().getConfig();
    return config.apiBaseUrl;
  }

  static Future<Map<String, String>> getHeaders() async {
    final config = await APIConfigLoader().getConfig();
    final basicAuth = 'Basic ' + base64Encode(
        utf8.encode('${config.apiUsername}:${config.apiPassword}')
    );
    return <String, String>{'authorization': basicAuth};
  }

  static Future<List<dynamic>> getCameras() async {
    final url = await getBaseUrl() + "/cameras";
    final headers = await getHeaders();

    try {
      final response = await http.get(url, headers: headers);
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load cameras: ' + response.body);
      }
    } catch (error) {
      // TODO: wrap with Result and handle error higher
      throw error;
    }
  }

  static Future<Map<String, dynamic>> getCameraEvents(String cameraUid,
      {int page = 1, int page_size = 20}) async {
    final url = await getBaseUrl() + "/cameras/${cameraUid}/events/?page=${page.toString()}&page_size=${page_size.toString()}";
    final headers = await getHeaders();

    try {

      final response = await http.get(url, headers: headers);
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load camera events: ' + response.body);
      }
    } catch (error) {
      // TODO: wrap with Result and handle error higher
      throw error;
    }
  }
}
