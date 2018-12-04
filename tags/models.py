from sqlalchemy.event import listens_for

from app import db, es


class Tag(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)

    def __repr__(self):
        return self.name

    @classmethod
    def search(cls, text):
        search_body = {
            "query": {
                "percolate": {
                    "field": "query",
                    "document": {
                        "name": text
                    }
                }
            }
        }
        indxs = es.connection.search(index="tag", doc_type="tag", body=search_body)

        tag_ids = [int(hit['_id']) for hit in indxs['hits']['hits']]

        return cls.query.filter(cls.id.in_(tag_ids)).all()


@listens_for(Tag, "after_insert")
@listens_for(Tag, 'after_update')
def after_insert_update(mapper, connection, target):
    body = {
        "query": {
            "match_phrase": {
                "name": {
                    "query": target.name,
                    "slop": 2
                }
            }
        }
    }

    es.connection.index(index="tag", doc_type="tag", id=target.id, body=body)


@listens_for(Tag, "after_delete")
def after_delete(mapper, connection, target):
    es.connection.delete(index="tag", doc_type="tag", id=target.id)

