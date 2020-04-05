from django.urls import path

from ekirill.cameras.api.views import CamerasList, CameraEventsList


app_name = 'cameras'

urlpatterns = [
    path('', CamerasList.as_view()),
    path('<uid>/', CameraEventsList.as_view()),
]
