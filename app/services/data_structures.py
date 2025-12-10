from typing import Any, Callable, Iterable, List, Optional


class BSTNode:
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None


class BinarySearchTree:
    def __init__(self, key_fn: Callable[[Any], Any]):
        self.root: Optional[BSTNode] = None
        self.key_fn = key_fn

    def insert(self, value: Any) -> None:
        key = self.key_fn(value)
        if self.root is None:
            self.root = BSTNode(key, value)
            return

        current = self.root
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = BSTNode(key, value)
                    return
                current = current.left
            elif key > current.key:
                if current.right is None:
                    current.right = BSTNode(key, value)
                    return
                current = current.right
            else:
                # Replace existing value when the key matches
                current.value = value
                return

    def find(self, key: Any) -> Optional[Any]:
        current = self.root
        while current:
            if key == current.key:
                return current.value
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    def inorder(self) -> List[Any]:
        ordered: List[Any] = []

        def _walk(node: Optional[BSTNode]) -> None:
            if not node:
                return
            _walk(node.left)
            ordered.append(node.value)
            _walk(node.right)

        _walk(self.root)
        return ordered

    @classmethod
    def from_iterable(cls, iterable: Iterable[Any], key_fn: Callable[[Any], Any]):
        tree = cls(key_fn)
        for value in iterable:
            tree.insert(value)
        return tree


class OrderNode:
    def __init__(self, order: Any):
        self.order = order
        self.next: Optional["OrderNode"] = None


class OrderLinkedList:
    def __init__(self, orders: Optional[Iterable[Any]] = None):
        self.head: Optional[OrderNode] = None
        self.tail: Optional[OrderNode] = None
        if orders:
            for order in orders:
                self.append(order)

    def append(self, order: Any) -> Any:
        new_node = OrderNode(order)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return order

        assert self.tail is not None
        self.tail.next = new_node
        self.tail = new_node
        return order

    def find(self, order_id: str) -> Optional[Any]:
        current = self.head
        while current:
            if current.order.get("id") == order_id:
                return current.order
            current = current.next
        return None

    def update(self, order_id: str, new_order: Any) -> Optional[Any]:
        current = self.head
        while current:
            if current.order.get("id") == order_id:
                current.order = new_order
                return new_order
            current = current.next
        return None

    def delete(self, order_id: str) -> bool:
        current = self.head
        previous: Optional[OrderNode] = None
        while current:
            if current.order.get("id") == order_id:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if current is self.tail:
                    self.tail = previous
                return True
            previous = current
            current = current.next
        return False

    def to_list(self) -> List[Any]:
        values: List[Any] = []
        current = self.head
        while current:
            values.append(current.order)
            current = current.next
        return values
