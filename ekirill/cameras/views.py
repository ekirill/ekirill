import datetime
import os

import pytz
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from django.conf import settings


class CamerasList(ListAPIView):
    class CameraSerializer(serializers.Serializer):
        id = serializers.CharField(source='pk')
        caption = serializers.CharField(required=True)

    serializer_class = CameraSerializer

    def get_queryset(self):
        for dirpath, dirnames, files in os.walk(settings.CAMERAS_VIDEO_DIR):
            return [
                {
                    'pk': _dir,
                    'caption': _dir,
                }
                for _dir in sorted(dirnames)
            ]


class CameraEventsList(ListAPIView):
    class CameraEventSerializer(serializers.Serializer):
        id = serializers.CharField(source='pk')
        start_timestamp = serializers.IntegerField()
        end_timestamp = serializers.IntegerField()
        url = serializers.CharField()

    serializer_class = CameraEventSerializer

    def get_queryset(self):
        camera_id = self.kwargs.get(self.lookup_field)
        camera_videos_path = os.path.join(settings.CAMERAS_VIDEO_DIR, camera_id)
        if not os.path.exists(camera_videos_path):
            return []

        events = []
        for dirpath, dirnames, files in os.walk(camera_videos_path):
            for filename in files:
                if not filename.endswith('.mp4'):
                    continue

                file_size = os.path.getsize(os.path.join(dirpath, filename))
                duration = min(120, max(3, int(file_size / 1024 / 700)))
                dt_parts = filename.split('_')
                if len(dt_parts) < 4:
                    continue

                year, month, day, tm, *_ = dt_parts
                tz = pytz.timezone('Europe/Moscow')
                try:
                    start_dt = datetime.datetime(
                        int(year), int(month), int(day), int(tm[:2]), int((tm[2:4])), tzinfo=tz
                    )
                except (ValueError, TypeError):
                    continue

                start_timestamp = start_dt.timestamp()
                events.append({
                    'pk': filename,
                    'start_timestamp': start_timestamp,
                    'end_timestamp': start_timestamp + duration,
                    'url': '',
                })

        return list(sorted(events, key=lambda e: e['start_timestamp'], reverse=True))
