import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from ..services.data_structures import BinarySearchTree

BASE_DIR = Path(__file__).resolve().parents[2]
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
_tree: Optional[BinarySearchTree] = None


def _load_products() -> List[Dict]:
    if not PRODUCTS_FILE.exists():
        return []
    try:
        raw = PRODUCTS_FILE.read_bytes().decode("utf-8-sig").strip()
        return json.loads(raw) if raw else []
    except json.JSONDecodeError:
        return []


def _save_products(products: List[Dict]) -> None:
    PRODUCTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PRODUCTS_FILE.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")


def _build_tree(products: List[Dict]) -> BinarySearchTree:
    tree = BinarySearchTree(key_fn=lambda p: p["id"])
    for product in products:
        tree.insert(product)
    return tree


def _ensure_tree() -> BinarySearchTree:
    global _tree
    if _tree is None:
        _tree = _build_tree(_load_products())
    return _tree


def list_products() -> List[Dict]:
    tree = _ensure_tree()
    return tree.inorder()


def get_product(product_id: str) -> Optional[Dict]:
    tree = _ensure_tree()
    return tree.find(product_id)


def create_product(data: Dict) -> Dict:
    tree = _ensure_tree()

    new_product = {
        "id": data.get("id", str(uuid.uuid4())),
        "name": data["name"],
        "description": data.get("description", ""),
        "price": float(data["price"]),
        "stock": int(data.get("stock", 0)),
    }

    if tree.find(new_product["id"]):
        raise ValueError("Ya existe un producto con ese ID")

    tree.insert(new_product)
    # Persist the in-order traversal so the JSON stays aligned with the BST content
    _save_products(tree.inorder())
    return new_product
