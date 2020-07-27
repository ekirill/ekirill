class Camera {
  final String uid;
  final String caption;
  final String thumb;

  Camera(this.uid, this.caption, this.thumb);

  Camera.fromJson(Map<String, dynamic> json)
      : uid = json['uid'], caption = json['caption'], thumb = json['thumb'];
}


class CameraList {
  final List<Camera> items;

  CameraList(this.items);

  CameraList.fromJson(List<dynamic> jsonList)
      : items = jsonList.map((item) => Camera.fromJson(item)).toList();
}