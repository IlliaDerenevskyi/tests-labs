import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.discount_calculator import DiscountCalculator

scenarios("../features/discount.feature")


@given(
    parsers.re(r"товар коштує (?P<price>-?\d+) грн"),
    converters={"price": int},
    target_fixture="price",
)
def product_price(price):
    return price


@given(parsers.parse("знижка становить {discount:d} відсотків"), target_fixture="discount")
def discount_percent(discount):
    return discount


@when("система розраховує фінальну ціну", target_fixture="calculation_result")
def calculate_price(price, discount):
    calculator = DiscountCalculator()
    try:
        return {"value": calculator.calculate(price, discount), "error": None}
    except (TypeError, ValueError) as error:
        return {"value": None, "error": error}


@then(parsers.parse("результат повинен становити {expected:d} грн"))
def check_price(calculation_result, expected):
    assert calculation_result["error"] is None
    assert calculation_result["value"] == pytest.approx(expected)


@then(parsers.parse('система повинна відхилити розрахунок з помилкою "{message}"'))
def check_error(calculation_result, message):
    assert calculation_result["value"] is None
    assert str(calculation_result["error"]) == message
