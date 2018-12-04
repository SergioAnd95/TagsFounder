import pytest

from app import create_app, db, es, elasticsearch_setup

from tags.models import Tag


def get_fixture_data():
    fixtures = [
        Tag(name='Toyota'),
        Tag(name='Toyota Corolla 2007'),
        Tag(name='Toyota Corolla LE'),
        Tag(name='4 Wheel Drive'),
        Tag(name='Air Conditioner')
    ]
    return fixtures


@pytest.fixture(scope="session")
def app():
    app = create_app(object_config='settings.settings.TestConfig')
    with app.app_context():
        db.create_all()
        elasticsearch_setup()
        for tag in get_fixture_data():
            db.session.add(tag)
            db.session.commit()
        yield app
        es.connection.indices.delete(index='*')

        db.session.remove()
        db.drop_all()
