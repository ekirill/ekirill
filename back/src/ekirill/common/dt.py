import datetime
from typing import Union

from ekirill.core.config import app_config


def is_aware(dt: datetime.datetime) -> bool:
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def make_aware(dt: Union[datetime.datetime, datetime.date]) -> Union[datetime.datetime, datetime.date]:
    """
    Adds timezone to `dt`, is this is naive datetime
    """
    if isinstance(dt, datetime.date):
        return dt

    if is_aware(dt):
        return dt

    return app_config.tzinfo.localize(dt)
