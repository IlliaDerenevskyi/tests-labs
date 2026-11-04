import pytest

from src.temperature_converter import TemperatureConverter


@pytest.mark.parametrize(
    ("celsius", "fahrenheit"),
    [(0, 32.0), (100, 212.0), (-40, -40.0), (-273.15, -459.67)],
)
def test_celsius_to_fahrenheit(celsius, fahrenheit):
    result = TemperatureConverter.celsius_to_fahrenheit(celsius)
    assert result == pytest.approx(fahrenheit)


@pytest.mark.parametrize(
    ("fahrenheit", "celsius"),
    [(32, 0.0), (212, 100.0), (-40, -40.0), (-459.67, -273.15)],
)
def test_fahrenheit_to_celsius(fahrenheit, celsius):
    result = TemperatureConverter.fahrenheit_to_celsius(fahrenheit)
    assert result == pytest.approx(celsius)


@pytest.mark.parametrize("value", ["10", None, [1], True])
def test_celsius_to_fahrenheit_rejects_non_numbers(value):
    with pytest.raises(TypeError, match="Temperature must be a number"):
        TemperatureConverter.celsius_to_fahrenheit(value)


@pytest.mark.parametrize("value", ["10", None, [1], True])
def test_fahrenheit_to_celsius_rejects_non_numbers(value):
    with pytest.raises(TypeError, match="Temperature must be a number"):
        TemperatureConverter.fahrenheit_to_celsius(value)


def test_celsius_below_absolute_zero_raises_error():
    with pytest.raises(ValueError, match="below absolute zero"):
        TemperatureConverter.celsius_to_fahrenheit(-273.16)


def test_fahrenheit_below_absolute_zero_raises_error():
    with pytest.raises(ValueError, match="below absolute zero"):
        TemperatureConverter.fahrenheit_to_celsius(-459.68)
