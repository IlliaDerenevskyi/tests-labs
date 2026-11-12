class Product:
    def __init__(self, name, price, category="General", discount_percent=0):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty")
        if type(price) not in (int, float) or not 0 < price < float("inf"):
            raise ValueError("Price must be greater than zero")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category cannot be empty")

        self.name = name.strip()
        self.price = round(price, 2)
        self.category = category.strip()
        self.discount_percent = 0
        self.set_discount(discount_percent)

    def set_discount(self, percent):
        if type(percent) not in (int, float) or not 0 <= percent <= 50:
            raise ValueError("Discount must be between 0 and 50")
        self.discount_percent = percent

    def get_final_price(self):
        return round(self.price * (1 - self.discount_percent / 100), 2)

    def is_in_category(self, category):
        return self.category.lower() == category.strip().lower()
