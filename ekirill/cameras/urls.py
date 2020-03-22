from django.urls import path

from ekirill.cameras.views import CamerasList, CameraEventsList


urlpatterns = [
    path('', CamerasList.as_view()),
    path('<pk>/', CameraEventsList.as_view()),
]
