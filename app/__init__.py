from flask import Flask
from .config import Configuration
from .extensions import api as smorest_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    smorest_api.init_app(app)

    from .api.orders import blp as OrdersBlueprint

    smorest_api.register_blueprint(OrdersBlueprint)

    @app.route("/")
    def index():
        return (
            "<!doctype html>"
            "<html lang='en'>"
            "<head><meta charset='utf-8'><title>Orders API</title></head>"
            "<body style='font-family: Arial, sans-serif; max-width: 760px; margin: 40px auto;'>"
            "<h1>Orders & Products API</h1>"
            "<p>Estado: <strong>OK</strong></p>"
            "<ul>"
            "<li><a href='/docs'>Swagger / OpenAPI UI</a></li>"
            "<li><a href='/openapi.json'>Descargar OpenAPI JSON</a></li>"
            "<li><a href='/health'>Healthcheck JSON</a></li>"
            "</ul>"
            "<p>Los datos se almacenan en JSON usando arboles BST para productos y listas enlazadas para pedidos.</p>"
            "</body></html>"
        )

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "orders-api"}, 200

    return app
