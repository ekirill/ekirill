import 'package:flutter/material.dart';

import 'api.dart';
import 'models/camera.dart';

class MyCameras extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
            'Видеонаблюдение EKirill',
            style: Theme.of(context).textTheme.headline6
        ),
      ),
      body: _CamerasList(),
    );
  }
}


class _CamerasList extends StatefulWidget {
  @override
  __CamerasListState createState() => __CamerasListState();
}

class __CamerasListState extends State<_CamerasList> {
  Future<CameraList> futureCamerasData;

  @override
  void initState() {
    super.initState();
    futureCamerasData = CamerasAPI.getCameras();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<CameraList>(
        future: futureCamerasData,
        // ignore: missing_return
        builder: (BuildContext context, AsyncSnapshot<CameraList> snapshot) {
          if (snapshot.hasData) {
            final tiles = snapshot.data.items.map(
                    (Camera camera) {
                  List<Widget> cameraChildren = [
                    ListTile(
                      leading: Icon(Icons.camera_alt, size: 50),
                      title: Text(camera.caption),
                    )
                  ];
                  if (camera.thumb != null) {
                    cameraChildren.add(
                        FittedBox(
                          child: Image.network(
                            // workaround to refresh camera images
                            '${camera.thumb}?v=${new DateTime.now().millisecondsSinceEpoch}',
                            width: 864,
                            height: 480,
                          ),
                          fit: BoxFit.fitWidth,
                        )
                    );
                  }
                  return Card(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(5.0),
                    ),
                    elevation: 3,
                    child: InkWell(
                      onTap: () {
                        Navigator.of(context).pushNamed(
                          '/events',
                          arguments: camera.uid,
                        );
                      },
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: cameraChildren,
                      ),
                    ),
                  );
                }
            ).toList();
            return _buildRefreshIndicator(
              child: ListView(
                  padding: const EdgeInsets.only(top: 10.0),
                  children: tiles
              )
            );
          } else if (snapshot.hasError) {
            return Text("${snapshot.error}");
          }
          return Center(
              child: CircularProgressIndicator()
          );
        }
    );
  }

  Widget _buildRefreshIndicator({Widget child}) {
    if (child == null) {
      child = Container();
    }
    return Center(
        child: RefreshIndicator(
          onRefresh: () async {
            setState(() {
                this.futureCamerasData = CamerasAPI.getCameras();
            });
          },
          child: child,
        )
    );
  }
}
