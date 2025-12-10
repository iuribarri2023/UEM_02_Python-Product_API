import json
from pathlib import Path
from typing import Dict, List, Optional

from ..services.data_structures import OrderLinkedList

BASE_DIR = Path(__file__).resolve().parents[2]
ORDERS_FILE = BASE_DIR / "data" / "orders.json"
_linked_list: Optional[OrderLinkedList] = None


def _load_orders() -> List[Dict]:
    if not ORDERS_FILE.exists():
        return []
    try:
        raw = ORDERS_FILE.read_bytes().decode("utf-8-sig").strip()
        return json.loads(raw) if raw else []
    except json.JSONDecodeError:
        return []


def _save_orders(orders: List[Dict]) -> None:
    ORDERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    ORDERS_FILE.write_text(json.dumps(orders, ensure_ascii=False, indent=2), encoding="utf-8")


def _build_linked_list() -> OrderLinkedList:
    orders = _load_orders()
    return OrderLinkedList(orders)


def _ensure_linked_list() -> OrderLinkedList:
    global _linked_list
    if _linked_list is None:
        _linked_list = _build_linked_list()
    return _linked_list


def list_orders() -> List[Dict]:
    linked_list = _ensure_linked_list()
    return linked_list.to_list()


def get_order(order_id: str) -> Optional[Dict]:
    linked_list = _ensure_linked_list()
    return linked_list.find(order_id)


def create_order(order: Dict) -> Dict:
    linked_list = _ensure_linked_list()
    linked_list.append(order)
    _save_orders(linked_list.to_list())
    return order


def update_order(order_id: str, new_order: Dict) -> Optional[Dict]:
    linked_list = _ensure_linked_list()
    updated = linked_list.update(order_id, new_order)
    if updated:
        _save_orders(linked_list.to_list())
    return updated


def delete_order(order_id: str) -> bool:
    linked_list = _ensure_linked_list()
    deleted = linked_list.delete(order_id)
    if deleted:
        _save_orders(linked_list.to_list())
    return deleted
