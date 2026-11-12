class ShoppingCart:
    def __init__(self):
        self._items = {}
        self._coupon_percent = 0

    def add_product(self, product, quantity=1):
        self._check_quantity(quantity)
        self._items[product] = self._items.get(product, 0) + quantity

    def remove_product(self, product, quantity=None):
        if product not in self._items:
            raise ValueError("Product is not in cart")

        if quantity is None:
            del self._items[product]
            return

        self._check_quantity(quantity)
        if quantity > self._items[product]:
            raise ValueError("Cannot remove more than in cart")

        self._items[product] -= quantity
        if self._items[product] == 0:
            del self._items[product]

    def set_coupon(self, percent):
        if type(percent) not in (int, float) or not 0 <= percent <= 20:
            raise ValueError("Coupon must be between 0 and 20")
        self._coupon_percent = percent

    def get_items(self):
        return self._items.copy()

    def get_total(self):
        subtotal = sum(
            product.get_final_price() * quantity
            for product, quantity in self._items.items()
        )
        return round(subtotal * (1 - self._coupon_percent / 100), 2)

    def get_item_count(self):
        return sum(self._items.values())

    def is_empty(self):
        return len(self._items) == 0

    def clear(self):
        self._items.clear()
        self._coupon_percent = 0

    @staticmethod
    def _check_quantity(quantity):
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
