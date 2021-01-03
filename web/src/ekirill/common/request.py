from django.conf import settings


def get_base_url() -> str:
    return '{proto}://{hostname}'.format(
        proto='https' if settings.IS_HTTPS else 'http',
        hostname=settings.HOSTNAME,
    )


def make_absolute_url(full_path: str) -> str:
    return get_base_url() + full_path
