import pytest

from shop.inventory import Inventory
from shop.product import Product


@pytest.fixture
def laptop():
    return Product("Laptop", 30000)


@pytest.fixture
def mouse():
    return Product("Mouse", 500)


@pytest.fixture
def inventory():
    return Inventory()


def test_add_new_product(inventory, laptop):
    inventory.add_product(laptop, 5)

    assert inventory.get_quantity(laptop) == 5


def test_adding_product_again_increases_quantity(inventory, laptop):
    inventory.add_product(laptop, 5)
    inventory.add_product(laptop, 3)

    assert inventory.get_quantity(laptop) == 8


def test_unknown_product_has_zero_quantity(inventory, laptop):
    assert inventory.get_quantity(laptop) == 0


def test_is_available_true_when_enough_stock(inventory, laptop):
    inventory.add_product(laptop, 5)

    assert inventory.is_available(laptop, 5) is True
    assert inventory.is_available(laptop, 2) is True


def test_is_available_false_when_not_enough_stock(inventory, laptop):
    inventory.add_product(laptop, 2)

    assert inventory.is_available(laptop, 3) is False
    assert inventory.is_available(Product("Unknown", 1), 1) is False


def test_remove_product_decreases_quantity(inventory, laptop):
    inventory.add_product(laptop, 5)

    inventory.remove_product(laptop, 2)

    assert inventory.get_quantity(laptop) == 3


def test_remove_more_than_in_stock_raises_error(inventory, laptop):
    inventory.add_product(laptop, 2)

    with pytest.raises(ValueError, match="Not enough stock"):
        inventory.remove_product(laptop, 3)

    assert inventory.get_quantity(laptop) == 2


def test_remove_last_unit_leaves_zero(inventory, laptop):
    inventory.add_product(laptop, 1)

    inventory.remove_product(laptop, 1)

    assert inventory.get_quantity(laptop) == 0


@pytest.mark.parametrize("quantity", [0, -1, 1.5, "1", None, True])
def test_add_invalid_quantity_raises_error(inventory, laptop, quantity):
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        inventory.add_product(laptop, quantity)


@pytest.mark.parametrize("quantity", [0, -1])
def test_remove_invalid_quantity_raises_error(inventory, laptop, quantity):
    inventory.add_product(laptop, 5)

    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        inventory.remove_product(laptop, quantity)


@pytest.mark.parametrize("quantity", [0, -1])
def test_is_available_invalid_quantity_raises_error(inventory, laptop, quantity):
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        inventory.is_available(laptop, quantity)


def test_default_low_stock_limit_is_three():
    assert Inventory().low_stock_limit == 3


def test_custom_low_stock_limit():
    assert Inventory(low_stock_limit=10).low_stock_limit == 10


@pytest.mark.parametrize("limit", [-1, 1.5, "3", None])
def test_invalid_low_stock_limit_raises_error(limit):
    with pytest.raises(ValueError, match="Low stock limit cannot be negative"):
        Inventory(low_stock_limit=limit)


def test_low_stock_products_are_returned(inventory, laptop, mouse):
    inventory.add_product(laptop, 2)
    inventory.add_product(mouse, 10)

    assert inventory.get_low_stock_products() == [laptop]


def test_product_with_quantity_equal_to_limit_is_low_stock(inventory, laptop):
    inventory.add_product(laptop, 3)

    assert laptop in inventory.get_low_stock_products()


def test_product_with_quantity_above_limit_is_not_low_stock(inventory, laptop):
    inventory.add_product(laptop, 4)

    assert inventory.get_low_stock_products() == []


def test_product_with_zero_stock_after_removal_is_low_stock(inventory, laptop):
    inventory.add_product(laptop, 1)
    inventory.remove_product(laptop, 1)

    assert inventory.get_low_stock_products() == [laptop]
