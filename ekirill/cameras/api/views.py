from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from ekirill.cameras.services.cameras import get_cameras_list, get_camera_events


class CamerasList(ListAPIView):
    permission_classes = (IsAuthenticated,)

    class CameraSerializer(serializers.Serializer):
        uid = serializers.CharField(source='uid')
        caption = serializers.CharField(required=True)

    serializer_class = CameraSerializer

    def get_queryset(self):
        return get_cameras_list()


class CameraEventsList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'uid'

    class CameraEventSerializer(serializers.Serializer):
        uid = serializers.CharField(source='uid')
        start_timestamp = serializers.IntegerField()
        end_timestamp = serializers.IntegerField()
        url = serializers.CharField()

    serializer_class = CameraEventSerializer

    def get_queryset(self):
        camera_uid = self.kwargs.get(self.lookup_url_kwarg)
        if not camera_uid:
            raise NotFound()

        events = get_camera_events(camera_uid)
        if events is None:
            raise NotFound()

        return get_camera_events(camera_uid)
