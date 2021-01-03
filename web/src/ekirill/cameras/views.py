from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from ekirill.cameras import repository
from ekirill.common.auth import staff_required


@staff_required
def cameras_list(request: HttpRequest) -> HttpResponse:
    context = {
        'cameras': repository.get_cameras_list()
    }
    return render(request, "cameras_list.html", context)


@staff_required
def camera_events_list(request: HttpRequest, camera_uid: str) -> HttpResponse:
    context = {
        'camera': repository.get_camera(camera_uid),
        'events': repository.get_camera_events(camera_uid),
    }
    return render(request, "camera_events_list.html", context)


@staff_required
def camera_event(request: HttpRequest, camera_uid: str, event_uid: str) -> HttpResponse:
    context = {
        'camera': repository.get_camera(camera_uid),
        'event': repository.get_camera_event(camera_uid, event_uid),
    }
    return render(request, "camera_event.html", context)


def camera_thumb(request: HttpRequest, camera_uid: str) -> HttpResponse:
    response = HttpResponse(status=200)
    response['Content-Type'] = 'image/jpeg'
    response['X-Accel-Redirect'] = repository.get_camera_thumbnail_xaccel_path(camera_uid)
    return response


def camera_event_video(request: HttpRequest, camera_uid: str, event_uid: str) -> HttpResponse:
    response = HttpResponse(status=200)
    response['Content-Type'] = 'video/mp4'
    response['X-Accel-Redirect'] = repository.get_camera_event_xaccel_path(camera_uid, event_uid)
    return response


def camera_event_thumb(request: HttpRequest, camera_uid: str, event_uid: str) -> HttpResponse:
    response = HttpResponse(status=200)
    response['Content-Type'] = 'image/jpeg'
    response['X-Accel-Redirect'] = repository.get_camera_event_thumbnail_xaccel_path(camera_uid, event_uid)
    return response
