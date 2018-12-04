import os

from envparse import env


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_file = os.environ.get('ENV_FILE_PATH', default=os.path.join(BASE_DIR, 'settings/.env'))
if os.path.isfile(env_file):
    env.read_envfile(env_file)


INSTALLED_APPS = (
    'tags',
)


class BaseConfig:
    DEBUG = env.bool('DEBUG', default=True)
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL', default=os.path.join(BASE_DIR, 'db.sqlite'))
    ELASTICSEARCH_URL = env.list('ELASTICSEARCH_URL', default=[])
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = env.str('TEST_DATABASE_URL', default=os.path.join(BASE_DIR, 'db.sqlite'))
    ELASTICSEARCH_URL = env.list('TEST_ELASTICSEARCH_URL', default=[])
