import 'package:flutter/material.dart';
import 'mycameras/mycameras.dart';
import 'myevents/myevents.dart';
import 'myeventvideo/myeventvideo.dart';

void main() {
  runApp(EKCamera());
}

class EKCamera extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EK Camera',
      theme: ThemeData(
        primarySwatch: Colors.deepOrange,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      onGenerateRoute: (RouteSettings settings) {
        var routes = <String, WidgetBuilder>{
          '/': (context) => MyCameras(),
          '/cameras': (context) => MyCameras(),
          '/events': (context) => MyEvents(settings.arguments),
          '/events/view': (context) => MyEventVideo(settings.arguments),
        };
        WidgetBuilder builder = routes[settings.name];
        return MaterialPageRoute(builder: (ctx) => builder(ctx));
      },
    );
  }
}
