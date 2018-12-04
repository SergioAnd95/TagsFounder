from settings import settings


def discover_urls(api):
    """
    Find and register all apps routes
    from apps
    :return: list
    """

    for app in settings.INSTALLED_APPS:
        try:
            _temp = __import__(f'{app}.urls', globals(), locals(), ['urlpatterns'], 0)
        except ModuleNotFoundError:
            pass
        else:
            for url in _temp.urlpatterns:
                api.add_resource(*url)
