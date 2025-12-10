import uuid
from typing import Dict, List, Optional, Tuple

from ..repositories import order_repository, product_repository


def _resolve_items(items: List[Dict]) -> Tuple[List[Dict], float]:
    resolved: List[Dict] = []
    total = 0.0

    for item in items:
        product_id = item["product_id"]
        quantity = int(item.get("quantity", 1))
        if quantity < 1:
            raise ValueError("La cantidad debe ser mayor o igual que 1")

        product = product_repository.get_product(product_id)
        if not product:
            raise ValueError(f"Producto no encontrado: {product_id}")

        line_total = float(product["price"]) * quantity
        resolved.append(
            {
                "product_id": product_id,
                "quantity": quantity,
                "product": product,
                "line_total": round(line_total, 2),
            }
        )
        total += line_total

    return resolved, round(total, 2)


def create_order(data: Dict) -> Dict:
    items, total = _resolve_items(data["items"])
    order = {
        "id": str(uuid.uuid4()),
        "customer_name": data["customer_name"],
        "items": items,
        "total": total,
    }
    return order_repository.create_order(order)


def get_order(order_id: str) -> Optional[Dict]:
    return order_repository.get_order(order_id)


def list_orders() -> List[Dict]:
    return order_repository.list_orders()


def update_order(order_id: str, updates: Dict) -> Optional[Dict]:
    existing = order_repository.get_order(order_id)
    if not existing:
        return None

    new_order = existing.copy()
    if "customer_name" in updates:
        new_order["customer_name"] = updates["customer_name"]

    if "items" in updates:
        items, total = _resolve_items(updates["items"])
        new_order["items"] = items
        new_order["total"] = total

    return order_repository.update_order(order_id, new_order)


def delete_order(order_id: str) -> bool:
    return order_repository.delete_order(order_id)
