from marshmallow import Schema, fields


class TagFinderSchema(Schema):
    text = fields.Str()
