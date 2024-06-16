from main import settings


def get_backend_url() -> str:
    return '{0}://{1}:{2}'.format(
        settings.HTTP_PROTOCOL,
        settings.HOST,
        settings.PORT
    )

def get_url(path: str = '/') -> str:
    return '{}{}'.format(
        get_backend_url(),
        path
    )

