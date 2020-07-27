import 'dart:math';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'api.dart';
import 'models/events.dart';


class MyEvents extends StatefulWidget {
  final String cameraUid;

  MyEvents(this.cameraUid);

  @override
  _MyEventsState createState() => _MyEventsState();
}

class _MyEventsState extends State<MyEvents> {
  final dtFormat = DateFormat('MMMM, dd H:m');
  List<Event> events = [];
  ScrollController _scrollController = new ScrollController();
  int _loadedPages = 0;
  bool _isFetching = false;

  @override
  void initState() {
    super.initState();
    fetch();
    _scrollController.addListener(_scrollStateListener);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollStateListener() {
    if (_scrollController.position.pixels == _scrollController.position.maxScrollExtent) {
      // We are at the end of list
      fetch();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Камера ' + widget.cameraUid,
          style: Theme.of(context).textTheme.headline6
        ),
      ),
      body: ListView.builder(
        controller: _scrollController,
        padding: const EdgeInsets.only(top: 10.0),
        itemCount: _getListLength(),
        itemBuilder: (BuildContext context, int index) {
          if (_isFetching && index ==  _getListLength() - 1) {
            return Center(
                child: CircularProgressIndicator()
            );
          }
          return _buildEventCard(events[index]);
        },
      ),
    );
  }

  int _getListLength() {
    int len = events.length;
    if (_isFetching) {
      len += 1;
    }
    return len;
  }

  Card _buildEventCard(Event event) {
    List<Widget> cameraChildren = [
      ListTile(
        leading: Icon(Icons.camera_alt, size: 50),
        title: Text(dtFormat.format(event.startTime)),
        subtitle: Text(event.duration.toString() + 'сек'),
      )
    ];
    if (event.thumb != null) {
      cameraChildren.add(
          FittedBox(
            child: Image.network(
              event.thumb,
              width: 320,
              height: 180,
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
            '/events/view',
            arguments: event.video,
          );
        },
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: cameraChildren,
        ),
      ),
    );
  }

  fetch() async {
    setState(() {
      _isFetching = true;
    });
    final eventsList =
        await CameraEventsAPI.getCameraEvents(widget.cameraUid, page: _loadedPages + 1);
    setState(() {
      _loadedPages = max(eventsList.page, _loadedPages);
      _isFetching = false;
      events.addAll(eventsList.items);
      _scrollStateListener();
    });
  }
}
