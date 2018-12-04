from elasticsearch5 import Elasticsearch as Es
from flask import current_app, _app_ctx_stack as stack


class Elasticsearch(object):
    """An Elasticsearch connector
    Your application's configuration will need the following parameters:
        * ``ELASTICSEARCH_CONNECTION``: a comma-separated list of URLs,
                                        defaults to `http://127.0.0.1:9200`.
        * ``ELASTICSEARCH_USERNAME``: the username to connect with, if any;
                                      defaults to `''`.
        * ``ELASTICSEARCH_PASSWORD``: the password to use, if any;
                                      defaults to `''`.
        * ``ELASTICSEARCH_USE_SSL``: whether to use SSL for the connection,
                                     defaults to `False`.
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('ELASTICSEARCH_URL',
                              'http://127.0.0.1:9200')
        app.config.setdefault('ELASTICSEARCH_USERNAME', '')
        app.config.setdefault('ELASTICSEARCH_PASSWORD', '')
        app.config.setdefault('ELASTICSEARCH_USE_SSL', False)
        # Use the new style teardown_appcontext if it's available,
        # otherwise fall back to the request context.
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        return Es(
            current_app.config['ELASTICSEARCH_URL'],
            http_auth=(current_app.config['ELASTICSEARCH_USERNAME'],
                       current_app.config['ELASTICSEARCH_PASSWORD']),
            use_ssl=current_app.config['ELASTICSEARCH_USE_SSL'],
            sniff_on_start=True,
            sniff_on_connection_fail=True
        )

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'es'):
            ctx.es = None

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'es'):
                ctx.es = self.connect()
            return ctx.es