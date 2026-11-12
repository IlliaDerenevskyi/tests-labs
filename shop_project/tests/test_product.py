import pytest

from shop.product import Product


def test_product_is_created_with_name_and_price():
    product = Product("Keyboard", 1000)

    assert product.name == "Keyboard"
    assert product.price == 1000


def test_product_is_created_with_name_price_and_category():
    product = Product("  Laptop ", 30000, category=" Electronics ")

    assert product.name == "Laptop"
    assert product.price == 30000
    assert product.category == "Electronics"
    assert product.discount_percent == 0


def test_product_default_category_is_general():
    assert Product("Pen", 10).category == "General"


@pytest.mark.parametrize("name", ["", "   ", None, 123])
def test_product_with_invalid_name_raises_error(name):
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product(name, 100)


def test_product_with_zero_price_raises_error():
    with pytest.raises(ValueError):
        Product("Keyboard", 0)


@pytest.mark.parametrize("price", [-1, -0.01, "100", None, float("inf"), True])
def test_product_with_invalid_price_raises_error(price):
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        Product("Keyboard", price)


@pytest.mark.parametrize("category", ["", "   ", None])
def test_product_with_invalid_category_raises_error(category):
    with pytest.raises(ValueError, match="Category cannot be empty"):
        Product("Keyboard", 100, category=category)


def test_price_is_rounded_to_two_decimals():
    assert Product("Item", 10.999).price == 11.0


def test_set_discount_changes_final_price():
    product = Product("Keyboard", 1000)
    product.set_discount(10)

    assert product.discount_percent == 10
    assert product.get_final_price() == 900


@pytest.mark.parametrize(
    ("price", "discount", "expected"),
    [(1000, 0, 1000), (1000, 10, 900), (200, 50, 100), (99.99, 15, 84.99)],
)
def test_get_final_price(price, discount, expected):
    product = Product("Item", price, discount_percent=discount)

    assert product.get_final_price() == expected


def test_zero_discount_keeps_original_price():
    product = Product("Keyboard", 1000)
    product.set_discount(0)

    assert product.get_final_price() == 1000


@pytest.mark.parametrize("percent", [50.01, 51, 100, -1, -0.5, "10", None])
def test_invalid_discount_raises_error(percent):
    product = Product("Keyboard", 1000)

    with pytest.raises(ValueError, match="Discount must be between 0 and 50"):
        product.set_discount(percent)

    assert product.discount_percent == 0


def test_invalid_discount_in_constructor_raises_error():
    with pytest.raises(ValueError, match="Discount must be between 0 and 50"):
        Product("Keyboard", 1000, discount_percent=60)


def test_is_in_category_matches_category():
    product = Product("Laptop", 30000, category="Electronics")

    assert product.is_in_category("Electronics") is True
    assert product.is_in_category("Books") is False


@pytest.mark.parametrize("query", ["electronics", "ELECTRONICS", "  Electronics  "])
def test_is_in_category_ignores_case_and_spaces(query):
    product = Product("Laptop", 30000, category="Electronics")

    assert product.is_in_category(query) is True
