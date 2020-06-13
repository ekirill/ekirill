import pytz
from environs import Env

default_env = Env()
# Read .env into os.environ, if exists
default_env.read_env()


class DBSettings:
    def __init__(self, env):
        with env.prefixed('DEFAULT_'):
            self.name = env('NAME', 'ekirill')
            self.host = env('HOST', 'localhost')
            self.user = env('USER', 'test')
            self.password = env('PASSWORD', 'test')


class DB:
    def __init__(self, env):
        with env.prefixed('DB_'):
            self.default = DBSettings(env)


class Camera:
    def __init__(self, env):
        with env.prefixed('CAMERA_'):
            self.videodir = env('VIDEODIR')


class Webdav:
    def __init__(self, env):
        with env.prefixed('WEBDAV_'):
            self.login = env('LOGIN', '')
            self.password = env('PASSWORD', '')


class GoogleOAuthSettings:
    def __init__(self, env):
        with env.prefixed('GOOGLE_OAUTH2_'):
            self.key = env('KEY', '')
            self.secret = env('SECRET', '')


class Auth:
    def __init__(self, env):
        with env.prefixed('AUTH_'):
            self.google = GoogleOAuthSettings(env)


class AppConfig:
    def __init__(self, env=default_env):
        with env.prefixed('EKIRILL_'):
            self.base_url = env('BASE_URL')
            self.secret = env('SECRET', 'dev_secret')
            self.port = env('BACKEND_PORT', 8176)
            self.tz = env('TZ', 'Europe/Moscow')
            self.tzinfo = pytz.timezone(self.tz)

            self.webdav = Webdav(env)
            self.db = DB(env)
            self.camera = Camera(env)
            self.auth = Auth(env)


app_config = AppConfig()
