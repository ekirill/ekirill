from django.urls import path
from ekirill.cameras.api import views


urlpatterns = [
    path('', views.CamerasList.as_view(), name='api_cameras_list'),
    path('<camera_uid>/events/', views.CameraEventsList.as_view(), name='api_camera_events_list'),
]
