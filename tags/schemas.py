from flask_restplus import fields

from app import api


TagCreateRetrieveSchema = api.model('Tag', {
    'name': fields.String(required=True)
})


TagFindSchema = api.model('Text', {
    'text': fields.String(required=True)
})
