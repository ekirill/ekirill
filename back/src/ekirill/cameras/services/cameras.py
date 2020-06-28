import datetime
import os
from typing import List, Optional

from ekirill.cameras import schemas
from ekirill.cameras.exceptions import CameraDoesNotExist
from ekirill.common.dt import make_aware
from ekirill.core.config import app_config


def get_camera_thumb_file(camera_uid: str) -> Optional[str]:
    thumb_file = os.path.join(app_config.camera.videodir, camera_uid, app_config.camera.default_thumb_filename)
    if os.path.exists(thumb_file):
        return thumb_file


def get_camera_event_file(camera_uid: str, event_uid: str) -> Optional[str]:
    event_file = os.path.join(app_config.camera.videodir, camera_uid, event_uid)
    if os.path.exists(event_file):
        return event_file


def get_camera(camera_uid: str) -> schemas.Camera:
    camera_data = {
        "uid": camera_uid,
        "caption": camera_uid,
    }
    thumb_file = get_camera_thumb_file(camera_uid)
    if thumb_file:
        from ekirill.app import app
        camera_data["thumb"] = \
            app.url_path_for('camera_thumb', camera_uid=camera_uid).make_absolute_url(app_config.base_url)
    return schemas.Camera(**camera_data)


def get_cameras_list() -> List[schemas.Camera]:
    for dirpath, dirnames, files in os.walk(app_config.camera.videodir):
        return [
            get_camera(_dir) for _dir in sorted(dirnames)
        ]


def get_camera_event(camera_uid, event_uid) -> Optional[schemas.CameraEvent]:
    if not event_uid.endswith('.mp4'):
        return None

    file_size = os.path.getsize(os.path.join(app_config.camera.videodir, camera_uid, event_uid))
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

    return schemas.CameraEvent(
        uid=event_uid,
        start_time=start_dt,
        end_time=start_dt + datetime.timedelta(seconds=duration),
        duration=duration,
    )


def get_camera_events(camera_uid: str) -> List[schemas.CameraEvent]:
    camera_videos_path = os.path.join(app_config.camera.videodir, camera_uid)
    if not os.path.exists(camera_videos_path):
        raise CameraDoesNotExist()

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
    return os.path.join(app_config.camera.videodir, camera_uid, event_uid)


def get_event_internal_url(camera_uid, event_uid):
    return os.path.join(camera_uid, event_uid)
