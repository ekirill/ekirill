import pytz
import datetime
import os
from typing import NamedTuple, List

from django.conf import settings


class Camera(NamedTuple):
    uid: str
    caption: str


class CameraEvent(NamedTuple):
    uid: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: int
    url: str


def get_cameras_list() -> List[Camera]:
    for dirpath, dirnames, files in os.walk(settings.CAMERAS_VIDEO_DIR):
        return [
            Camera(
                uid=_dir,
                caption=_dir,
            )
            for _dir in sorted(dirnames)
        ]


def get_camera_events(camera_uid: str) -> List[CameraEvent]:
    camera_videos_path = os.path.join(settings.CAMERAS_VIDEO_DIR, camera_uid)
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

            events.append({
                'uid': filename,
                'start_time': start_dt,
                'end_time': start_dt + datetime.timedelta(seconds=duration),
                'duration': duration,
                'url': '#',
            })

        # walking only root folder
        break

    events = sorted(events, key=lambda e: e['start_time'], reverse=True)

    return [CameraEvent(**ev) for ev in events]
