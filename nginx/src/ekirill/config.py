import pytz
from environs import Env

default_env = Env()
# Read .env into os.environ, if exists
default_env.read_env()


class Thumbnails:
    def __init__(self, env):
        with env.prefixed('THUMB_'):
            self.ext = env('EXT', 'jpg')
            self.width = env.int('WIDTH', 320)
            self.height = env.int('HEIGHT', 180)


class Storage:
    def __init__(self, env):
        with env.prefixed('STORAGE_'):
            self.dir = env('DIR')
            self.max_size_gb = env.float('MAX_SIZE_GB')
            self.recheck_every = env.int('RECHECK_EVERY', 60)
            self.full_recheck_every = env.int('FULL_RECHECK_EVERY', 3600)


class AppConfig:
    def __init__(self, env=default_env):
        with env.prefixed('EKIRILL_'):
            self.tz = env('TZ', 'Europe/Moscow')
            self.tzinfo = pytz.timezone(self.tz)
            self.log_file = env('LOG', '/dev/stdout')

            self.storage = Storage(env)
            self.thumbnails = Thumbnails(env)


app_config = AppConfig()
