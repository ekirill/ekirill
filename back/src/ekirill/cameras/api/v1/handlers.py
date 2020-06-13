from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ekirill.cameras import schemas
from ekirill.cameras.exceptions import CameraDoesNotExist
from ekirill.cameras.services.cameras import get_cameras_list, get_camera_events
from ekirill.common.pagination.per_page_paginator import Paginator
from ekirill.common.schemas import ApiError

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.Camera],
    responses={
        200: {
            "description": "List of available cameras",
        }
    }
)
def cameras_list():
    return get_cameras_list()


@router.get(
    "/{camera_uid}/events/",
    response_model=schemas.PaginatedCameraEvents,
    responses={
        200: {"description": "List of events for the selected camera"},
        404: {"model": ApiError},
    }
)
def camera_events(camera_uid: str, paginator: Paginator = Depends(Paginator)):
    try:
        events = get_camera_events(camera_uid)
        paginated = paginator.paginate(events)

        return paginated
    except CameraDoesNotExist:
        return JSONResponse(status_code=404, content={"detail": "Camera not found"})
