class Event {
  final String uid;
  final DateTime startTime;
  final DateTime endTime;
  final int duration;
  final String video;
  final String thumb;

  Event(this.uid, this.startTime, this.endTime, this.duration, this.video,
      this.thumb);

  Event.fromJson(Map<String, dynamic> json)
      : uid = json['uid'],
        startTime = DateTime.parse(json['start_time']),
        endTime = DateTime.parse(json['start_time']),
        duration = json['duration'],
        video = json['video'],
        thumb = json['thumb'];
}

class EventsList {
  final List<Event> items;
  final int page;

  EventsList(this.items, this.page);

  EventsList.fromJson(Map<String, dynamic> json, this.page)
      : items = json['items']
            .map((item) => Event.fromJson(item))
            .toList()
            .cast<Event>();
}
