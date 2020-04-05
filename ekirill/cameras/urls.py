from django.urls import path

from ekirill.cameras.views import CamerasListView, CameraEventsView


app_name = 'cameras'

urlpatterns = [
    path('', CamerasListView.as_view(), name='cameras-list'),
    path('<uid>/', CameraEventsView.as_view(), name='camera-events'),
]
