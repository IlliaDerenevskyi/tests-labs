class OrderService:
    def __init__(self, inventory):
        self.inventory = inventory
        self._orders = []
        self._next_order_id = 1

    def create_order(self, cart):
        if cart.is_empty():
            raise ValueError("Cart is empty")

        items = cart.get_items()

        # Спочатку перевіряємо УСІ товари; нічого не списуємо.
        for product, quantity in items.items():
            if not self.inventory.is_available(product, quantity):
                raise ValueError(f"Not enough stock for {product.name}")

        total = cart.get_total()

        for product, quantity in items.items():
            self.inventory.remove_product(product, quantity)

        order = {
            "id": self._next_order_id,
            "status": "created",
            "total": total,
            "items": [
                {"name": product.name, "quantity": quantity}
                for product, quantity in items.items()
            ],
        }
        self._orders.append(order)
        self._next_order_id += 1
        cart.clear()
        return order.copy()

    def get_order(self, order_id):
        for order in self._orders:
            if order["id"] == order_id:
                return order.copy()
        raise ValueError("Order not found")

    def get_order_count(self):
        return len(self._orders)
