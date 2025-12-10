from marshmallow import Schema, fields, validate
from .product_schemas import ProductSchema


class OrderItemSchema(Schema):
    product_id = fields.String(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))


class OrderItemDetailSchema(Schema):
    product_id = fields.String()
    quantity = fields.Integer()
    product = fields.Nested(ProductSchema)
    line_total = fields.Float()


class OrderSchema(Schema):
    id = fields.String()
    customer_name = fields.String()
    items = fields.List(fields.Nested(OrderItemDetailSchema))
    total = fields.Float()


class OrderCreateSchema(Schema):
    customer_name = fields.String(required=True)
    items = fields.List(
        fields.Nested(OrderItemSchema),
        required=True,
        validate=validate.Length(min=1),
    )


class OrderUpdateSchema(Schema):
    customer_name = fields.String()
    items = fields.List(
        fields.Nested(OrderItemSchema),
        validate=validate.Length(min=1),
    )
