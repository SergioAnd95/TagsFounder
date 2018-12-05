from app import api, db

from werkzeug.exceptions import BadRequest

from flask_restplus import Resource
from sqlalchemy.exc import IntegrityError


from .schemas import TagCreateRetrieveSchema, TagFindSchema
from .models import Tag


@api.route('/tags')
class TagListCreateView(Resource):
    """
    Endpoint for get list tags or create tag
    """
    @api.marshal_with(TagCreateRetrieveSchema)
    def get(self):
        tags = Tag.query.all()
        return tags

    @api.expect(TagCreateRetrieveSchema, validate=True)
    @api.marshal_with(TagCreateRetrieveSchema)
    def post(self):
        data = self.api.payload
        tag = Tag(**data)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            raise BadRequest(f'Tag with name "{tag.name}" already exist')

        return tag, 201


@api.route('/tags_find')
class TagsSearchView(Resource):
    """
    Endpoint for find tags in text
    """
    @api.expect(TagFindSchema, validate=True)
    @api.marshal_with(TagCreateRetrieveSchema)
    def post(self):
        data = self.api.payload

        tags_find = Tag.search(text=data['text'])
        return tags_find, 200
