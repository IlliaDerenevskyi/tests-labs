---
title: Звіт до лабораторної роботи №3
permalink: /lab3/
---

# Звіт до лабораторної роботи №3

## Тема

**Назва лабораторної роботи:** Методи Assert, верифікація та валідація вхідних даних.

## Мета роботи

Навчитися перевіряти результат роботи Python-коду за допомогою pytest, тестувати правильні й неправильні вхідні дані та пройти практичні цикли TDD і BDD.

## Структура проєкту

```text
lab_assert_validation/
├── src/
│   ├── __init__.py
│   ├── bank_account.py
│   ├── temperature_converter.py
│   ├── user_registration_validator.py
│   └── discount_calculator.py
├── tests/
│   ├── test_bank_account.py
│   ├── test_temperature_converter.py
│   ├── test_user_registration.py
│   └── test_discount_calculator.py
├── features/
│   ├── user_registration.feature
│   └── discount.feature
├── requirements-dev.txt
└── pytest.ini
```

Конфігурація `pytest.ini`:

```ini
[pytest]
pythonpath = .
```

## TDD: BankAccount

Клас розроблявся циклом RED → GREEN → REFACTOR. Спочатку був написаний тест поповнення, який не проходив, бо `deposit()` нічого не змінював. Далі `deposit()` отримав мінімальну реалізацію, потім негативний тест (сума `0`) знову дав RED і був доведений до GREEN перевіркою `amount <= 0`. На етапі REFACTOR однакову перевірку з `deposit()` і `withdraw()` винесено в метод `_validate_positive_amount`.

### Етап RED

![Скріншот №1 — RED](./screen1.png)

### Етап GREEN

![Скріншот №2 — GREEN](./screen2.png)

### Етап REFACTOR

![Скріншот №3 — REFACTOR](./screen3.png)

### Реалізація `src/bank_account.py`

```python
class BankAccount:
    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance

    @staticmethod
    def _validate_positive_amount(amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def deposit(self, amount):
        self._validate_positive_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        self._validate_positive_amount(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def get_balance(self):
        return self._balance
```

### Тести `tests/test_bank_account.py`

```python
import pytest

from src.bank_account import BankAccount


def test_new_account_has_zero_balance():
    assert BankAccount().get_balance() == 0


def test_account_with_initial_balance():
    assert BankAccount(250).get_balance() == 250


def test_negative_initial_balance_raises_error():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-1)


def test_deposit_adds_money():
    account = BankAccount()
    account.deposit(100)
    assert account.get_balance() == 100


@pytest.mark.parametrize("amount", [0, -50])
def test_deposit_non_positive_amount_raises_error(amount):
    account = BankAccount()
    with pytest.raises(ValueError, match="Amount must be positive"):
        account.deposit(amount)
    assert account.get_balance() == 0


def test_withdraw_subtracts_money():
    account = BankAccount(200)
    account.withdraw(75)
    assert account.get_balance() == 125


@pytest.mark.parametrize("amount", [0, -10])
def test_withdraw_non_positive_amount_raises_error(amount):
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Amount must be positive"):
        account.withdraw(amount)
    assert account.get_balance() == 100


def test_withdraw_more_than_balance_raises_error():
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(100.01)
    assert account.get_balance() == 100
```

## TDD: TemperatureConverter

Розробка велася невеликими циклами: перший тест `0 °C → 32 °F` (RED через `NotImplementedError`), мінімальна формула (GREEN), потім перетворення в зворотний бік, перевірка типу та абсолютного нуля. Для чисел із плаваючою крапкою використано `pytest.approx()`, для винятків — `pytest.raises()`.

### Реалізація `src/temperature_converter.py`

```python
class TemperatureConverter:
    @staticmethod
    def _validate_number(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("Temperature must be a number")

    @staticmethod
    def celsius_to_fahrenheit(value):
        TemperatureConverter._validate_number(value)
        if value < -273.15:
            raise ValueError("Temperature is below absolute zero")
        return value * 9 / 5 + 32

    @staticmethod
    def fahrenheit_to_celsius(value):
        TemperatureConverter._validate_number(value)
        if value < -459.67:
            raise ValueError("Temperature is below absolute zero")
        return (value - 32) * 5 / 9
```

### Тести `tests/test_temperature_converter.py`

```python
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
```

## BDD: UserRegistrationValidator

### Файл `features/user_registration.feature`

![Скріншот №4 — feature-файл](./screen4.png)

```gherkin
Feature: Реєстрація користувача

  Scenario: Коректні дані користувача
    Given користувач вводить email "student@example.com"
    And користувач вводить пароль "password1"
    And користувачу 20 років
    When система перевіряє реєстраційні дані
    Then реєстраційні дані повинні бути прийняті

  Scenario: Email без частини після символу @
    Given користувач вводить email "student@"
    And користувач вводить пароль "password1"
    And користувачу 20 років
    When система перевіряє реєстраційні дані
    Then система повинна відхилити дані з помилкою "Email is invalid"

  Scenario: Пароль коротший за 8 символів
    Given користувач вводить email "student@example.com"
    And користувач вводить пароль "pass1"
    And користувачу 20 років
    When система перевіряє реєстраційні дані
    Then система повинна відхилити дані з помилкою "Password must contain at least 8 characters"

  Scenario: Пароль без цифри
    Given користувач вводить email "student@example.com"
    And користувач вводить пароль "password"
    And користувачу 20 років
    When система перевіряє реєстраційні дані
    Then система повинна відхилити дані з помилкою "Password must contain a digit"

  Scenario: Вік менший за 18 років
    Given користувач вводить email "student@example.com"
    And користувач вводить пароль "password1"
    And користувачу 17 років
    When система перевіряє реєстраційні дані
    Then система повинна відхилити дані з помилкою "Age must be between 18 and 120"
```

### Step definitions `tests/test_user_registration.py`

![Скріншот №5 — кроки Given/When/Then](./screen5.png)

```python
from pytest_bdd import given, parsers, scenarios, then, when

from src.user_registration_validator import UserRegistrationValidator

scenarios("../features/user_registration.feature")


@given(parsers.parse('користувач вводить email "{email}"'), target_fixture="email")
def user_email(email):
    return email


@given(parsers.parse('користувач вводить пароль "{password}"'), target_fixture="password")
def user_password(password):
    return password


@given(parsers.parse("користувачу {age:d} років"), target_fixture="age")
def user_age(age):
    return age


@when("система перевіряє реєстраційні дані", target_fixture="validation_result")
def validate_user(email, password, age):
    validator = UserRegistrationValidator()
    try:
        validator.validate(email, password, age)
        return {"accepted": True, "error": None}
    except (TypeError, ValueError) as error:
        return {"accepted": False, "error": error}


@then("реєстраційні дані повинні бути прийняті")
def registration_is_accepted(validation_result):
    assert validation_result["accepted"] is True
    assert validation_result["error"] is None


@then(parsers.parse('система повинна відхилити дані з помилкою "{message}"'))
def registration_is_rejected(validation_result, message):
    assert validation_result["accepted"] is False
    assert str(validation_result["error"]) == message
```

Спочатку крок `When` не обробляв виняток, тому негативний сценарій аварійно завершувався з `ValueError`. Після того як помилка почала повертатися як дані (`{"accepted": False, "error": error}`), крок `Then` порівнює її текст з очікуваним.

![Скріншот №6 — невдалий негативний сценарій](./screen6.png)

## BDD: DiscountCalculator

### Файл `features/discount.feature`

```gherkin
Feature: Розрахунок знижки

  Scenario: Знижка 20 відсотків
    Given товар коштує 1000 грн
    And знижка становить 20 відсотків
    When система розраховує фінальну ціну
    Then результат повинен становити 800 грн

  Scenario: Знижка 0 відсотків не змінює ціну
    Given товар коштує 1000 грн
    And знижка становить 0 відсотків
    When система розраховує фінальну ціну
    Then результат повинен становити 1000 грн

  Scenario: Знижка 100 відсотків
    Given товар коштує 1000 грн
    And знижка становить 100 відсотків
    When система розраховує фінальну ціну
    Then результат повинен становити 0 грн

  Scenario: Від'ємна ціна
    Given товар коштує -100 грн
    And знижка становить 10 відсотків
    When система розраховує фінальну ціну
    Then система повинна відхилити розрахунок з помилкою "Price cannot be negative"

  Scenario: Знижка більша за 100 відсотків
    Given товар коштує 1000 грн
    And знижка становить 101 відсотків
    When система розраховує фінальну ціну
    Then система повинна відхилити розрахунок з помилкою "Discount must be between 0 and 100"
```

### Step definitions `tests/test_discount_calculator.py`

```python
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
```

Додано сценарії для знижок `0%` і `100%`, від'ємної ціни та знижки `101%`. Для негативних сценаріїв використано той самий прийом, що й для `UserRegistrationValidator`: помилка перехоплюється в `When` і перевіряється в `Then`.

## Результат

Фінальний запуск усіх тестів:

```bash
pytest -v
```

Усі 38 тестів (звичайні pytest-тести та BDD-сценарії) мають статус `PASSED`.

![Скріншот №7 — фінальний запуск](./screen7.png)

## Висновок

У лабораторній роботі через `assert` перевірялися фактичні результати (числа, булеві значення, повідомлення), через `pytest.raises()` — виняткові ситуації для некоректних даних. Цикл TDD (RED → GREEN → REFACTOR) застосовано для `BankAccount` і `TemperatureConverter`, а поведінку `UserRegistrationValidator` і `DiscountCalculator` описано сценаріями Given → When → Then у `pytest-bdd`. Валідація вхідних даних і верифікація результату перевірялися як позитивними, так і негативними тестами.
