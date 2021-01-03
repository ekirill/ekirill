from environs import Env

default_env = Env()
# Read .env into os.environ, if exists
default_env.read_env()


class Camera:
    def __init__(self, env):
        with env.prefixed('CAMERA_'):
            self.videodir = env('VIDEODIR')
            self.now_image_name = env('NOW_IMAGE_NAME', 'CURRENT.jpg')


class GoogleOAuthSettings:
    def __init__(self, env):
        with env.prefixed('GOOGLE_OAUTH2_'):
            self.key = env('KEY', '')
            self.secret = env('SECRET', '')


class BasicAPIAuthSettings:
    def __init__(self, env):
        with env.prefixed('APIBASIC_'):
            self.username = env('USERNAME', '')
            self.password = env('PASSWORD', '')


class Auth:
    def __init__(self, env):
        with env.prefixed('AUTH_'):
            self.google = GoogleOAuthSettings(env)
            self.api_basic = BasicAPIAuthSettings(env)


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


class EnvConf:
    def __init__(self, env=default_env):
        with env.prefixed('EKIRILL_WEB_'):
            self.camera = Camera(env)
            self.auth = Auth(env)
            self.db = DB(env)
            self.secret = env('SECRET', 'most_secure_secret')
            self.debug = env.bool('DEBUG', False)
            self.hostname = env('HOST', 'ekirill.ru')


env_conf = EnvConf()
