from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    stock = fields.Integer(required=True, validate=validate.Range(min=0))


class ProductCreateSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(load_default="")
    price = fields.Float(required=True, validate=validate.Range(min=0))
    stock = fields.Integer(load_default=0, validate=validate.Range(min=0))
