from urllib.parse import urlencode

from starlette.requests import Request


def get_absolute_url(request: Request):
    return f"{request.url.scheme}://{request.url.hostname}{request.url.path}"


def build_url_with_args(path: str, params: dict):
    return f"{path}?{urlencode(params)}"
