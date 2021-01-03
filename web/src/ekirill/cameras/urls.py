from django.urls import path
from ekirill.cameras import views


urlpatterns = [
    path('', views.cameras_list, name='cameras_list'),
    path('<camera_uid>/events/', views.camera_events_list, name='camera_events_list'),
    path('<camera_uid>/events/<event_uid>/', views.camera_event, name='camera_event'),

    path('<camera_uid>/thumb.jpg', views.camera_thumb, name='camera_thumb'),
    path('<camera_uid>/events/<event_uid>/video.mp4', views.camera_event_video, name='camera_event_video'),
    path('<camera_uid>/events/<event_uid>/thumb.jpg', views.camera_event_thumb, name='camera_event_thumb'),
]
