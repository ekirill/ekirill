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


class AppConfig:
    def __init__(self, env=default_env):
        with env.prefixed('EKIRILL_'):
            self.secret = env('SECRET', 'devsecret')
            self.db = DB(env)
            self.camera = Camera(env)


app_config = AppConfig()