# Orders & Products API

API REST con Flask que almacena productos en un arbol binario de busqueda (BST) y pedidos en una lista enlazada; los datos se serializan en archivos JSON.

## Endpoints principales
- `POST /v1/products` crear producto (name, price, stock, description opcional)
- `GET /v1/products` listar productos (in-order del BST)
- `GET /v1/products/{product_id}` obtener producto por ID desde el BST
- `POST /v1/orders` crear pedido con items `[ { product_id, quantity } ]`
- `GET /v1/orders` listar pedidos (recorrido de la lista enlazada)
- `GET /v1/orders/{order_id}` obtener pedido por ID
- `PATCH /v1/orders/{order_id}` actualizar cliente o items
- `DELETE /v1/orders/{order_id}` eliminar pedido

## Datos de ejemplo
- `data/products.json` contiene productos de construccion precargados.
- `data/orders.json` incluye pedidos que referencian esos productos; cada nodo de la lista enlazada almacena un pedido completo con sus items.

## Ejecutar en local
1. Crear entorno y dependencias: `pip install -r requirements.txt`
2. Iniciar el servidor: `python main.py`
3. Documentacion interactiva: `http://localhost:5000/docs`
