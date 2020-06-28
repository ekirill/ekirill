import uvicorn
from fastapi import FastAPI

from ekirill.cameras.api.v1.handlers import router as cameras_router_v1
from ekirill.core.config import app_config

app = FastAPI()

app.include_router(
    cameras_router_v1,
    prefix='/api/v1/cameras',
    tags=['cameras'],
)

if __name__ == "__main__":
    uvicorn.run(
        "ekirill.app:app",
        host="0.0.0.0",
        port=app_config.port,
        log_level="debug",
        reload=True,
        workers=2,
        limit_concurrency=5
    )
