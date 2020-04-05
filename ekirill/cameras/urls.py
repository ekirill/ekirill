from django.urls import path

from ekirill.cameras.views import CamerasListView, CameraEventsListView, CameraEventView, CameraEventDownloadView


app_name = 'cameras'

urlpatterns = [
    path('', CamerasListView.as_view(), name='cameras-list'),
    path('<uid>/', CameraEventsListView.as_view(), name='camera-events-list'),
    path('<camera_uid>/<event_uid>/', CameraEventView.as_view(), name='camera-event'),
    path('<camera_uid>/<event_uid>/download/', CameraEventDownloadView.as_view(), name='camera-event-download'),
]
