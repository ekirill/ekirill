import datetime
from typing import Union

from django.utils.timezone import get_current_timezone


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

    return get_current_timezone.localize(dt)
