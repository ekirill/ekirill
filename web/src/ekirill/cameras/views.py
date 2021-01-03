from django.http.request import HttpRequest
from django.http.response import HttpResponse

from ekirill.cameras.repository import (
    get_camera_event_thumbnail_xaccel_path,
    get_camera_event_xaccel_path,
    get_camera_thumbnail_xaccel_path,
)


def camera_thumb(request: HttpRequest, camera_uid: str):
    response = HttpResponse(status=200)
    response['Content-Type'] = 'image/jpeg'
    response['X-Accel-Redirect'] = get_camera_thumbnail_xaccel_path(camera_uid)
    return response


def camera_event_video(request: HttpRequest, camera_uid: str, event_uid: str):
    response = HttpResponse(status=200)
    response['Content-Type'] = 'video/mp4'
    response['X-Accel-Redirect'] = get_camera_event_xaccel_path(camera_uid, event_uid)
    return response


def camera_event_thumb(request: HttpRequest, camera_uid: str, event_uid: str):
    response = HttpResponse(status=200)
    response['Content-Type'] = 'image/jpeg'
    response['X-Accel-Redirect'] = get_camera_event_thumbnail_xaccel_path(camera_uid, event_uid)
    return response
