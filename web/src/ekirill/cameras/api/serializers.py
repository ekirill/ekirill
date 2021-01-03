from rest_framework import serializers


class Camera(serializers.Serializer):
    uid = serializers.CharField()
    caption = serializers.CharField()
    thumb = serializers.CharField()


class CameraEvent(serializers.Serializer):
    uid = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    duration = serializers.IntegerField()
    video = serializers.CharField()
    thumb = serializers.CharField(required=False)
