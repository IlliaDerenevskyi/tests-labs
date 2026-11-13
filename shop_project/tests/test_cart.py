import pytest

from shop.cart import ShoppingCart
from shop.product import Product


@pytest.fixture
def keyboard():
    return Product("Keyboard", 1000)


@pytest.fixture
def mouse():
    return Product("Mouse", 500)


@pytest.fixture
def cart():
    return ShoppingCart()


def test_new_cart_is_empty(cart):
    assert cart.is_empty() is True
    assert cart.get_items() == {}
    assert cart.get_item_count() == 0
    assert cart.get_total() == 0


def test_add_one_product(cart, keyboard):
    cart.add_product(keyboard)

    assert cart.get_items() == {keyboard: 1}
    assert cart.is_empty() is False


def test_add_two_different_products(cart, keyboard, mouse):
    cart.add_product(keyboard)
    cart.add_product(mouse, 2)

    assert cart.get_items() == {keyboard: 1, mouse: 2}


def test_adding_same_product_again_increases_quantity(cart, keyboard):
    cart.add_product(keyboard, 2)
    cart.add_product(keyboard, 3)

    assert cart.get_items() == {keyboard: 5}


def test_total_of_several_products(cart, keyboard, mouse):
    cart.add_product(keyboard)
    cart.add_product(mouse)

    assert cart.get_total() == 5000


def test_total_with_quantity_greater_than_one(cart, keyboard):
    cart.add_product(keyboard, 3)

    assert cart.get_total() == 3000


def test_remove_product_completely(cart, keyboard, mouse):
    cart.add_product(keyboard, 2)
    cart.add_product(mouse)

    cart.remove_product(keyboard)

    assert cart.get_items() == {mouse: 1}


def test_remove_product_partially(cart, keyboard):
    cart.add_product(keyboard, 3)

    cart.remove_product(keyboard, 1)

    assert cart.get_items() == {keyboard: 2}


def test_remove_all_quantity_removes_product(cart, keyboard):
    cart.add_product(keyboard, 2)

    cart.remove_product(keyboard, 2)

    assert cart.is_empty() is True


def test_remove_more_than_in_cart_raises_error(cart, keyboard):
    cart.add_product(keyboard, 2)

    with pytest.raises(ValueError, match="Cannot remove more than in cart"):
        cart.remove_product(keyboard, 3)

    assert cart.get_items() == {keyboard: 2}


def test_remove_product_not_in_cart_raises_error(cart, keyboard):
    with pytest.raises(ValueError, match="Product is not in cart"):
        cart.remove_product(keyboard)


@pytest.mark.parametrize("quantity", [0, -1])
def test_remove_non_positive_quantity_raises_error(cart, keyboard, quantity):
    cart.add_product(keyboard, 2)

    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        cart.remove_product(keyboard, quantity)


def test_item_count_sums_all_units(cart, keyboard, mouse):
    cart.add_product(keyboard, 2)
    cart.add_product(mouse, 3)

    assert cart.get_item_count() == 5


def test_clear_empties_cart(cart, keyboard, mouse):
    cart.add_product(keyboard, 2)
    cart.add_product(mouse)

    cart.clear()

    assert cart.is_empty() is True
    assert cart.get_item_count() == 0


@pytest.mark.parametrize("quantity", [0, -1, 1.5, "2", None, True])
def test_add_invalid_quantity_raises_error(cart, keyboard, quantity):
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        cart.add_product(keyboard, quantity)

    assert cart.is_empty() is True


def test_coupon_applies_discount_to_total(cart, keyboard):
    cart.add_product(keyboard)
    cart.set_coupon(10)

    assert cart.get_total() == 900


@pytest.mark.parametrize("percent", [20.01, 21, 100, -1, "10", None])
def test_invalid_coupon_raises_error(cart, percent):
    with pytest.raises(ValueError, match="Coupon must be between 0 and 20"):
        cart.set_coupon(percent)


@pytest.mark.parametrize("percent", [0, 20])
def test_coupon_boundaries_are_accepted(cart, keyboard, percent):
    cart.add_product(keyboard)
    cart.set_coupon(percent)

    assert cart.get_total() == 1000 * (1 - percent / 100)


def test_total_with_product_discount(cart):
    cart.add_product(Product("Keyboard", 1000, discount_percent=10), 2)

    assert cart.get_total() == 1800


def test_total_with_product_discount_and_coupon(cart):
    cart.add_product(Product("Monitor", 10000, discount_percent=10), 2)
    cart.set_coupon(10)

    assert cart.get_total() == 16200


def test_clear_resets_coupon(cart, keyboard):
    cart.add_product(keyboard)
    cart.set_coupon(10)

    cart.clear()
    cart.add_product(keyboard)

    assert cart.get_total() == 1000


def test_get_items_returns_copy(cart, keyboard, mouse):
    cart.add_product(keyboard, 2)

    items = cart.get_items()
    items[mouse] = 5
    items[keyboard] = 100

    assert cart.get_items() == {keyboard: 2}
