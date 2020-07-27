import '../api.dart';
import 'models/events.dart';

class CameraEventsAPI {
  static Future<EventsList> getCameraEvents(String cameraUid,
      {int page = 1, int page_size = 20}) async {
    final jsonData = await API.getCameraEvents(cameraUid, page: page, page_size: page_size);
    return EventsList.fromJson(jsonData, page);
  }
}
