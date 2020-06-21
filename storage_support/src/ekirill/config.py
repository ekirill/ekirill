import pytz
from environs import Env

default_env = Env()
# Read .env into os.environ, if exists
default_env.read_env()


class Camera:
    def __init__(self, env):
        with env.prefixed('CAMERA_'):
            self.videodir = env('VIDEODIR')
            self.max_size_gb = env('VIDEODIR_MAX_SIZE_GB')


class AppConfig:
    def __init__(self, env=default_env):
        with env.prefixed('EKIRILL_'):
            self.tz = env('TZ', 'Europe/Moscow')
            self.tzinfo = pytz.timezone(self.tz)

            self.camera = Camera(env)


app_config = AppConfig()
