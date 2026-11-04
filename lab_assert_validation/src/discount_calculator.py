class DiscountCalculator:
    def calculate(self, price, discount_percent):
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise TypeError("Price must be a number")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if not isinstance(discount_percent, (int, float)) or isinstance(discount_percent, bool):
            raise TypeError("Discount must be a number")
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        return price * (1 - discount_percent / 100)
