import pytest

from shop.cart import ShoppingCart
from shop.inventory import Inventory
from shop.order_service import OrderService
from shop.product import Product


@pytest.fixture
def inventory():
    return Inventory()


@pytest.fixture
def service(inventory):
    return OrderService(inventory)


@pytest.fixture
def cart():
    return ShoppingCart()


def test_successful_order(inventory, service, cart):
    laptop = Product("Laptop", 30000)
    cart.add_product(laptop, 2)
    inventory.add_product(laptop, 5)

    order = service.create_order(cart)

    assert order["status"] == "created"
    assert order["total"] == 60000
    assert order["items"] == [{"name": "Laptop", "quantity": 2}]
    assert inventory.get_quantity(laptop) == 3
    assert cart.is_empty() is True
    assert service.get_order_count() == 1
    assert service.get_order(order["id"]) == order


def test_order_with_not_enough_stock_fails(inventory, service, cart):
    laptop = Product("Laptop", 30000)
    cart.add_product(laptop, 3)
    inventory.add_product(laptop, 2)

    with pytest.raises(ValueError, match="Not enough stock for Laptop"):
        service.create_order(cart)

    assert inventory.get_quantity(laptop) == 2
    assert cart.get_items() == {laptop: 3}
    assert service.get_order_count() == 0


def test_order_with_several_products(inventory, service, cart):
    keyboard = Product("Keyboard", 1000)
    mouse = Product("Mouse", 500)
    inventory.add_product(keyboard, 10)
    inventory.add_product(mouse, 10)
    cart.add_product(keyboard, 2)
    cart.add_product(mouse, 1)

    order = service.create_order(cart)

    assert order["status"] == "created"
    assert order["total"] == 2500
    assert inventory.get_quantity(keyboard) == 8
    assert inventory.get_quantity(mouse) == 9
    assert cart.is_empty() is True


def test_empty_cart_cannot_be_ordered(service, cart):
    with pytest.raises(ValueError, match="Cart is empty"):
        service.create_order(cart)

    assert service.get_order_count() == 0


def test_order_with_product_discount_and_coupon(inventory, service, cart):
    monitor = Product("Monitor", 10000, discount_percent=10)
    inventory.add_product(monitor, 5)
    cart.add_product(monitor, 2)
    cart.set_coupon(10)

    order = service.create_order(cart)

    assert order["status"] == "created"
    assert order["total"] == 16200
    assert inventory.get_quantity(monitor) == 3
    assert cart.is_empty() is True


def test_not_enough_of_one_of_several_products_changes_nothing(
    inventory, service, cart
):
    keyboard = Product("Keyboard", 1000)
    mouse = Product("Mouse", 500)
    inventory.add_product(keyboard, 5)
    inventory.add_product(mouse, 1)
    cart.add_product(keyboard, 2)
    cart.add_product(mouse, 3)

    with pytest.raises(ValueError, match="Not enough stock for Mouse"):
        service.create_order(cart)

    assert inventory.get_quantity(keyboard) == 5
    assert inventory.get_quantity(mouse) == 1
    assert cart.is_empty() is False
    assert cart.get_item_count() == 5
    assert service.get_order_count() == 0


def test_cart_and_coupon_are_reset_after_order(inventory, service, cart):
    keyboard = Product("Keyboard", 1000)
    inventory.add_product(keyboard, 10)
    cart.add_product(keyboard, 3)
    cart.set_coupon(10)

    order = service.create_order(cart)

    assert order["total"] == 2700
    assert inventory.get_quantity(keyboard) == 7
    assert cart.is_empty() is True
    assert cart.get_item_count() == 0
    assert cart.get_total() == 0

    cart.add_product(keyboard, 1)
    assert cart.get_total() == 1000


def test_order_history(inventory):
    keyboard = Product("Keyboard", 1000)
    mouse = Product("Mouse", 500)
    inventory.add_product(keyboard, 5)
    inventory.add_product(mouse, 5)
    service = OrderService(inventory)
    cart1, cart2 = ShoppingCart(), ShoppingCart()
    cart1.add_product(keyboard, 2)
    cart2.add_product(mouse, 3)

    order1 = service.create_order(cart1)
    order2 = service.create_order(cart2)

    assert order1["status"] == order2["status"] == "created"
    assert order1["id"] != order2["id"]
    assert service.get_order_count() == 2
    assert service.get_order(order1["id"])["total"] == 2000
    assert service.get_order(order2["id"])["total"] == 1500
    assert inventory.get_quantity(keyboard) == 3
    assert inventory.get_quantity(mouse) == 2


def test_get_unknown_order_raises_error(service):
    with pytest.raises(ValueError, match="Order not found"):
        service.get_order(999)


def test_returned_order_is_a_copy(inventory, service, cart):
    keyboard = Product("Keyboard", 1000)
    inventory.add_product(keyboard, 5)
    cart.add_product(keyboard)

    order = service.create_order(cart)
    order["status"] = "hacked"

    assert service.get_order(order["id"])["status"] == "created"
