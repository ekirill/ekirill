from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.responses import Response

from ekirill.cameras import schemas
from ekirill.cameras.exceptions import CameraDoesNotExist
from ekirill.cameras.services.cameras import (
    get_camera_event_thumbnail_xaccel_path,
    get_camera_event_xaccel_path,
    get_camera_events,
    get_camera_thumbnail_xaccel_path,
    get_cameras_list,
)
from ekirill.common.pagination.per_page_paginator import Paginator
from ekirill.common.schemas import ApiError
from ekirill.core.auth import get_current_user

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
def cameras_list(user: str = Depends(get_current_user)):
    return get_cameras_list()


@router.get(
    "/{camera_uid}/events/",
    response_model=schemas.PaginatedCameraEvents,
    responses={
        200: {"description": "List of events for the selected camera"},
        404: {"model": ApiError},
    }
)
def camera_events(camera_uid: str, paginator: Paginator = Depends(Paginator), user: str = Depends(get_current_user)):
    try:
        events = get_camera_events(camera_uid)
        paginated = paginator.paginate(events)

        return paginated
    except CameraDoesNotExist:
        return JSONResponse(status_code=404, content={"detail": "Camera not found"})


@router.get("/{camera_uid}/thumb.jpg")
async def camera_thumb(camera_uid: str):
    return Response(
        status_code=200,
        headers={
            "X-Accel-Redirect": get_camera_thumbnail_xaccel_path(camera_uid)
        },
        media_type="image/jpeg",
    )


@router.get("/{camera_uid}/events/{event_uid}.mp4")
def camera_event(camera_uid: str, event_uid: str):
    return Response(
        status_code=200,
        headers={
            "X-Accel-Redirect": get_camera_event_xaccel_path(camera_uid, event_uid)
        },
        media_type="video/mp4",
    )


@router.get("/{camera_uid}/events/{event_uid}.jpg")
async def camera_event_thumb(camera_uid: str, event_uid: str):
    return Response(
        status_code=200,
        headers={
            "X-Accel-Redirect": get_camera_event_thumbnail_xaccel_path(camera_uid, event_uid)
        },
        media_type="image/jpeg",
    )
