class Inventory:
    def __init__(self, low_stock_limit=3):
        if type(low_stock_limit) is not int or low_stock_limit < 0:
            raise ValueError("Low stock limit cannot be negative")
        self._stock = {}
        self.low_stock_limit = low_stock_limit

    def add_product(self, product, quantity):
        self._check_quantity(quantity)
        self._stock[product] = self.get_quantity(product) + quantity

    def get_quantity(self, product):
        return self._stock.get(product, 0)

    def is_available(self, product, quantity):
        self._check_quantity(quantity)
        return self.get_quantity(product) >= quantity

    def remove_product(self, product, quantity):
        self._check_quantity(quantity)
        if not self.is_available(product, quantity):
            raise ValueError("Not enough stock")
        self._stock[product] -= quantity

    def get_low_stock_products(self):
        return [
            product for product, quantity in self._stock.items()
            if quantity <= self.low_stock_limit
        ]

    @staticmethod
    def _check_quantity(quantity):
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
