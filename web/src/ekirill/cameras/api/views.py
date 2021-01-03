from rest_framework.generics import ListAPIView

from ekirill.cameras.api import serializers
from ekirill.cameras import repository


class CamerasList(ListAPIView):
    serializer_class = serializers.Camera

    def get_queryset(self):
        return repository.get_cameras_list()


class CameraEventsList(ListAPIView):
    serializer_class = serializers.CameraEvent

    def get_queryset(self):
        return repository.get_camera_events(self.kwargs['camera_uid'])
