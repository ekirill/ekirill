import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class Camera(BaseModel):
    uid: str
    caption: str


class CameraEvent(BaseModel):
    uid: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: int


class PaginatedCameraEvents(BaseModel):
    previous: Optional[str]
    next: Optional[HttpUrl]
    items: List[CameraEvent]
