import datetime
import os
from typing import Optional, List

from django.conf import settings
from django.utils.timezone import make_aware
from django.urls import reverse

from ekirill.cameras.exceptions import CameraDoesNotExist
from ekirill.common.request import make_absolute_url
from ekirill.cameras import models as camera_models


def get_camera_thumb_file(camera_uid: str) -> Optional[str]:
    thumb_file = os.path.join(settings.CAMERA_VIDEODIR, camera_uid, settings.CAMERA_NOW_IMAGE_NAME)
    if os.path.exists(thumb_file):
        return thumb_file


def get_camera_thumbnail_xaccel_path(camera_uid: str) -> Optional[str]:
    return '/protected_cameras/' + os.path.join(camera_uid, settings.CAMERA_NOW_IMAGE_NAME)


def get_camera_event_file(camera_uid: str, event_uid: str) -> Optional[str]:
    event_file = os.path.join(settings.CAMERA_VIDEODIR, camera_uid, event_uid) + '.mp4'
    if os.path.exists(event_file):
        return event_file


def get_camera_event_xaccel_path(camera_uid: str, event_uid: str) -> Optional[str]:
    return '/protected_cameras/' + os.path.join(camera_uid, event_uid) + '.mp4'


def get_camera_event_thumbnail_file(camera_uid: str, event_uid: str) -> Optional[str]:
    thumbnail_file = os.path.join(settings.CAMERA_VIDEODIR, camera_uid, event_uid + '.mp4.jpg')
    if os.path.exists(thumbnail_file):
        return thumbnail_file


def get_camera_event_thumbnail_xaccel_path(camera_uid: str, event_uid: str) -> Optional[str]:
    return '/protected_cameras/' + os.path.join(camera_uid, event_uid) + '.mp4.jpg'


def get_camera(camera_uid: str) -> camera_models.Camera:
    camera_data = {
        "uid": camera_uid,
        "caption": camera_uid,
    }
    thumb_file = get_camera_thumb_file(camera_uid)
    if thumb_file:
        camera_data["thumb"] = make_absolute_url(
            reverse(
                'camera_thumb',
                kwargs={
                    'camera_uid': camera_uid
                },
            )
        )
    return camera_models.Camera(**camera_data)


def get_cameras_list() -> List[camera_models.Camera]:
    for dirpath, dirnames, files in os.walk(settings.CAMERA_VIDEODIR):
        return [get_camera(_dir) for _dir in sorted(dirnames)]


def get_camera_event(camera_uid, event_uid) -> Optional[camera_models.CameraEvent]:
    file_name = os.path.join(settings.CAMERA_VIDEODIR, camera_uid, event_uid) + '.mp4'
    if not os.path.exists(file_name):
        return None

    file_size = os.path.getsize(file_name)
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

    event_data = {
        'uid': event_uid,
        'start_time': start_dt,
        'end_time': start_dt + datetime.timedelta(seconds=duration),
        'duration': duration,
        'video': make_absolute_url(
            reverse(
                'camera_event_video',
                kwargs={
                    'camera_uid': camera_uid,
                    'event_uid': event_uid,
                },
            )
        ),
    }

    thumb_file = get_camera_event_thumbnail_file(camera_uid, event_uid)
    if thumb_file:
        event_data['thumb'] = make_absolute_url(
            reverse(
                'camera_event_thumb',
                kwargs={
                    'camera_uid': camera_uid,
                    'event_uid': event_uid,
                },
            )
        )
    else:
        event_data['thumb'] = None

    return camera_models.CameraEvent(**event_data)


def get_camera_events(camera_uid: str) -> List[camera_models.CameraEvent]:
    camera_videos_path = os.path.join(settings.CAMERA_VIDEODIR, camera_uid)
    if not os.path.exists(camera_videos_path):
        raise CameraDoesNotExist()

    events = []
    for dirpath, dirnames, files in os.walk(camera_videos_path):
        for filename in files:
            event_uid, _ = filename.rsplit('.', 1)
            ev = get_camera_event(camera_uid, event_uid)
            if not ev:
                continue
            events.append(ev)

        # walking only root folder
        break

    return list(sorted(events, key=lambda e: e.start_time, reverse=True))


def get_event_path(camera_uid, event_uid):
    return os.path.join(settings.CAMERA_VIDEODIR, camera_uid, event_uid)


def get_event_internal_url(camera_uid, event_uid):
    return os.path.join(camera_uid, event_uid)
