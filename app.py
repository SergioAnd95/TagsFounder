from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_cors import CORS

from core.utils import discover_urls
from core.elasticsearch import Elasticsearch


es = Elasticsearch()
db = SQLAlchemy()
api = Api()
cors = CORS()


def elasticsearch_setup():
    tag_settings = {
        "mappings": {
            "tag": {
                "properties": {
                    "name": {
                        "type": "text"
                    },
                    "query": {
                        "type": "percolator"
                    }
                }
            }
        }
    }
    es.connection.indices.create(index='tag', ignore=400, body=tag_settings)


def create_app(object_config='settings.settings.ProdConfig'):

    app = Flask(__name__)
    app.config.from_object(object_config)

    db.init_app(app)
    api.init_app(app)
    es.init_app(app)
    cors.init_app(app)

    with app.app_context():
        elasticsearch_setup()

    discover_urls(api)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
