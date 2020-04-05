import datetime
from typing import List, NamedTuple

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.views import View
from django.views.generic import TemplateView

from ekirill.cameras.services.cameras import (
    get_cameras_list, get_camera_events, get_event_internal_url,
    CameraEvent, Camera,
    get_camera_event, get_camera)


class CamerasListView(LoginRequiredMixin, TemplateView):
    template_name = 'cameras_list.html'

    def get_context_data(self, **kwargs):
        return {
            'cameras': get_cameras_list(),
        }


class DayEvents(NamedTuple):
    day: datetime.date
    events: List[CameraEvent]


class CameraEventsListView(LoginRequiredMixin, TemplateView):
    template_name = 'camera_events.html'

    def _group_events(self, events: List[CameraEvent]) -> List[DayEvents]:
        grouped_events = []

        current_day = events[0].start_time.date()
        day_events = []
        for ev in events:
            day = ev.start_time.date()
            if day != current_day:
                if day_events:
                    grouped_events.append(DayEvents(
                        day=current_day,
                        events=day_events,
                    ))
                current_day = day
                day_events = [ev]
            else:
                day_events.append(ev)

        if day_events:
            grouped_events.append(DayEvents(
                day=current_day,
                events=day_events,
            ))

        return grouped_events

    def get_context_data(self, **kwargs):
        camera_uid = kwargs.get('uid')
        if not camera_uid:
            raise Http404()

        events = get_camera_events(camera_uid)
        if events is None:
            raise Http404()

        grouped_events = self._group_events(events)

        return {
            'camera': get_camera(camera_uid),
            'events': grouped_events,
        }


class CameraEventDownloadView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        camera_uid = kwargs.get('camera_uid')
        event_uid = kwargs.get('event_uid')

        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename={}_{}".format(camera_uid, event_uid)
        response["X-Accel-Redirect"] = "/internal-camera/{}".format(get_event_internal_url(camera_uid, event_uid))

        return response


class CameraEventView(LoginRequiredMixin, TemplateView):
    template_name = 'camera_event.html'

    def get_context_data(self, **kwargs):
        camera_uid = kwargs.get('camera_uid')
        event_uid = kwargs.get('event_uid')

        return {
            'camera': get_camera(camera_uid),
            'event': get_camera_event(camera_uid, event_uid),
        }
