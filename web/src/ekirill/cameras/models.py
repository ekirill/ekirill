import datetime
from dataclasses import dataclass


@dataclass
class Camera:
    """Class for keeping meta info about camera in the system"""
    uid: str
    caption: str
    thumb: str


@dataclass
class CameraEvent:
    """Class for keeping meta info about event, that was recorded by the camera"""
    uid: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: int
    video: str
    thumb: str
