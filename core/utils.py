import importlib

from settings import settings


def autodiscover_app_modules(module_name):
    for app in settings.INSTALLED_APPS:
        importlib.import_module(f'{app}.{module_name}', '.')


