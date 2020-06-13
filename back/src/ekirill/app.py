from fastapi import FastAPI

from ekirill.cameras.api.v1.handlers import router as cameras_router_v1

app = FastAPI()

app.include_router(
    cameras_router_v1,
    prefix='/v1/cameras',
    tags=['cameras'],
)
