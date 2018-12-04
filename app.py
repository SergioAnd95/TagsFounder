from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_cors import CORS

from core.utils import autodiscover_app_modules
from core.elasticsearch import Elasticsearch


es = Elasticsearch()
db = SQLAlchemy()
api = Api()
cors = CORS()


def create_app(object_config='settings.settings.ProdConfig'):

    app = Flask(__name__)
    app.config.from_object(object_config)

    db.init_app(app)
    api.init_app(app)
    es.init_app(app)
    cors.init_app(app)

    autodiscover_app_modules('views')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
