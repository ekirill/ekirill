import 'dart:async' show Future;
import 'dart:convert' show json;
import 'package:flutter/services.dart' show rootBundle;

class ApiConfigData {
  final String apiBaseUrl;
  final String apiUsername;
  final String apiPassword;

  ApiConfigData({this.apiBaseUrl = "", this.apiUsername = "", this.apiPassword = ""});

  factory ApiConfigData.fromJson(Map<String, dynamic> jsonMap) {
    return new ApiConfigData(
      apiBaseUrl: jsonMap["api_baseurl"],
      apiUsername: jsonMap["api_username"],
      apiPassword: jsonMap["api_password"],
    );
  }
}


class SecretLoader {
  final String secretPath;

  SecretLoader({this.secretPath});
  Future<ApiConfigData> load() {
    return rootBundle.loadStructuredData<ApiConfigData>(
      this.secretPath,
      (jsonStr) async {
        final secret = ApiConfigData.fromJson(json.decode(jsonStr));
        return secret;
      }
    );
  }
}

class APIConfigLoader {
  // Config singleton
  APIConfigLoader._privateConstructor();
  static final APIConfigLoader _instance = APIConfigLoader._privateConstructor();
  ApiConfigData _data;

  factory APIConfigLoader() {
    return _instance;
  }

  Future<ApiConfigData> getConfig() async {
    if (_data == null) {
      _data = await SecretLoader(secretPath: "secrets.json").load();
    }
    return _data;
  }
}
