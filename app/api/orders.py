from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..repositories import product_repository
from ..schemas.order_schemas import OrderCreateSchema, OrderSchema, OrderUpdateSchema
from ..schemas.product_schemas import ProductCreateSchema, ProductSchema
from ..services import order_service

blp = Blueprint(
    "orders",
    "orders",
    url_prefix="/v1",
    description="Gestion de productos (BST) y pedidos (lista enlazada)",
)


@blp.route("/products")
class ProductCollection(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return product_repository.list_products()

    @blp.arguments(ProductCreateSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        try:
            return product_repository.create_product(product_data)
        except ValueError as exc:
            abort(400, message=str(exc))


@blp.route("/products/<string:product_id>")
class ProductResource(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        product = product_repository.get_product(product_id)
        if not product:
            abort(404, message="Producto no encontrado")
        return product


@blp.route("/orders")
class OrderCollection(MethodView):
    @blp.response(200, OrderSchema(many=True))
    def get(self):
        return order_service.list_orders()

    @blp.arguments(OrderCreateSchema)
    @blp.response(201, OrderSchema)
    def post(self, order_data):
        try:
            return order_service.create_order(order_data)
        except ValueError as exc:
            abort(400, message=str(exc))


@blp.route("/orders/<string:order_id>")
class OrderResource(MethodView):
    @blp.response(200, OrderSchema)
    def get(self, order_id):
        order = order_service.get_order(order_id)
        if not order:
            abort(404, message="Pedido no encontrado")
        return order

    @blp.arguments(OrderUpdateSchema)
    @blp.response(200, OrderSchema)
    def patch(self, updates, order_id):
        try:
            order = order_service.update_order(order_id, updates)
        except ValueError as exc:
            abort(400, message=str(exc))

        if not order:
            abort(404, message="Pedido no encontrado")
        return order

    @blp.response(204)
    def delete(self, order_id):
        deleted = order_service.delete_order(order_id)
        if not deleted:
            abort(404, message="Pedido no encontrado")
        return ""
