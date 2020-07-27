import '../api.dart';
import 'models/camera.dart';

class CamerasAPI {
  static Future<CameraList> getCameras() async {
    final jsonData = await API.getCameras();
    return CameraList.fromJson(jsonData);
  }
}
