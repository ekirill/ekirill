from functools import wraps
from typing import Callable
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url


def staff_required(view_func: Callable):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                return view_func(request, *args, **kwargs)

            return HttpResponseRedirect('/')

        path = request.build_absolute_uri()
        resolved_login_url = resolve_url(settings.LOGIN_URL)
        # If the login url is the same scheme and net location then just
        # use the path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
            path = request.get_full_path()
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(
            path, resolved_login_url, REDIRECT_FIELD_NAME)

    return _wrapped_view
