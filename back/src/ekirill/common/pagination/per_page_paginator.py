from typing import Collection

from starlette.requests import Request

from ekirill.common.server import build_url_with_args, get_absolute_url


class Paginator:
    def __init__(self, request: Request, page: int = 1, page_size: int = 20):
        self.request = request
        self.page = page
        self.page_size = page_size

    def paginate(self, collection: Collection) -> dict:
        pages = len(collection) // self.page_size
        if self.page_size * pages < len(collection):
            pages += 1

        answer = {
            "items": collection[(self.page - 1) * self.page_size:self.page * self.page_size],
        }

        api_path = get_absolute_url(self.request)
        if self.page > 1:
            answer['previous'] = build_url_with_args(api_path, {"page": self.page - 1})

        if self.page < pages:
            answer['next'] = build_url_with_args(api_path, {"page": self.page + 1})

        return answer
