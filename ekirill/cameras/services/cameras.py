import datetime
import os
from typing import NamedTuple, List

from django.conf import settings
from django.utils.timezone import make_aware


class Camera(NamedTuple):
    uid: str
    caption: str


class CameraEvent(NamedTuple):
    uid: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: int


def get_camera(camera_uid) -> Camera:
    return Camera(
        uid=camera_uid,
        caption=camera_uid,
    )


def get_cameras_list() -> List[Camera]:
    for dirpath, dirnames, files in os.walk(settings.CAMERAS_VIDEO_DIR):
        return [
            get_camera(_dir) for _dir in sorted(dirnames)
        ]


def get_camera_event(camera_uid, event_uid) -> CameraEvent:
    if not event_uid.endswith('.mp4'):
        return None

    file_size = os.path.getsize(os.path.join(settings.CAMERAS_VIDEO_DIR, camera_uid, event_uid))
    duration = min(120, max(3, int(file_size / 1024 / 700)))
    dt_parts = event_uid.split('_')
    if len(dt_parts) < 4:
        return None

    year, month, day, tm, *_ = dt_parts
    try:
        start_dt = datetime.datetime(
            int(year), int(month), int(day), int(tm[:2]), int((tm[2:4]))
        )
        make_aware(start_dt)
    except (ValueError, TypeError):
        return None

    return CameraEvent(
        uid=event_uid,
        start_time=start_dt,
        end_time=start_dt + datetime.timedelta(seconds=duration),
        duration=duration,
    )


def get_camera_events(camera_uid: str) -> List[CameraEvent]:
    camera_videos_path = os.path.join(settings.CAMERAS_VIDEO_DIR, camera_uid)
    if not os.path.exists(camera_videos_path):
        return []

    events = []
    for dirpath, dirnames, files in os.walk(camera_videos_path):
        for filename in files:
            ev = get_camera_event(camera_uid, filename)
            if not ev:
                continue
            events.append(ev)

        # walking only root folder
        break

    return list(sorted(events, key=lambda e: e.start_time, reverse=True))


def get_event_path(camera_uid, event_uid):
    return os.path.join(settings.CAMERAS_VIDEO_DIR, camera_uid, event_uid)


def get_event_internal_url(camera_uid, event_uid):
    return os.path.join(camera_uid, event_uid)
