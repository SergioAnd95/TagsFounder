import pytest

from core.elasticsearch import Elasticsearch
from app import create_app, elasticsearch_setup
from tags.models import *


def get_fixture_data():
    fixtures = [
        Tag(name='Toyota'),
        Tag(name='Toyota Corolla 2007'),
        Tag(name='Toyota Corolla LE'),
        Tag(name='4 Wheel Drive'),
        Tag(name='Air Conditioning')
    ]
    return fixtures


@pytest.fixture(scope='session')
def app():
    app = create_app(object_config='settings.settings.TestConfig')
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope='session')
def _db(app):

    db.app = app
    db.create_all()

    for tag in get_fixture_data():
        db.session.add(tag)
        db.session.commit()

    yield db
    db.drop_all()


@pytest.yield_fixture(scope='function')
def _es(app):
    es.app = app
    yield es


@pytest.fixture(scope='function', autouse=True)
def session(_db, _es):
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = _db.create_scoped_session(options=options)

    db.session = session_
    elasticsearch_setup()

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()
