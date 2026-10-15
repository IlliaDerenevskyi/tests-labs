import sys

import pytest

from conftest2 import account  # noqa: F401  (fixture from conftest2.py)
from src.main2 import BankAccount


def test_account_creation_with_balance_and_default_balance():
    acc = BankAccount("Ivan", 50)
    default = BankAccount("Olena")

    assert acc.owner == "Ivan"
    assert acc.balance == 50.0
    assert isinstance(acc.balance, float)
    assert default.balance == 0.0


def test_account_creation_accepts_zero_and_float_balance():
    assert BankAccount("Ivan", 0).get_balance() == 0.0
    assert BankAccount("Ivan", 10.5).get_balance() == 10.5


@pytest.mark.parametrize(
    ("args", "exc", "message"),
    [
        ((123, 10), TypeError, "Owner must be a string"),
        ((None,), TypeError, "Owner must be a string"),
        (("   ", 10), ValueError, "Owner name cannot be empty"),
        (("", 10), ValueError, "Owner name cannot be empty"),
        (("Ivan", "100"), TypeError, "Balance must be a number"),
        (("Ivan", -1), ValueError, "Initial balance cannot be negative"),
    ],
)
def test_account_creation_rejects_invalid_arguments(args, exc, message):
    with pytest.raises(exc, match=message):
        BankAccount(*args)


@pytest.mark.parametrize(
    ("amount", "expected"),
    [(50, 150.0), (0.5, 100.5), (1000, 1100.0)],
)
def test_deposit_increases_balance(account, amount, expected):
    account.deposit(amount)

    assert account.get_balance() == expected


def test_multiple_deposits_accumulate(account):
    account.deposit(10)
    account.deposit(20)

    assert account.balance == 130.0


@pytest.mark.parametrize("amount", [0, -5])
def test_deposit_rejects_non_positive_amount(account, amount):
    with pytest.raises(
        ValueError, match="Deposit amount must be greater than zero"
    ):
        account.deposit(amount)

    assert account.balance == 100.0


def test_deposit_rejects_non_numeric_amount(account):
    with pytest.raises(TypeError, match="Deposit amount must be a number"):
        account.deposit("50")


@pytest.mark.parametrize(
    ("amount", "expected"),
    [(30, 70.0), (100, 0.0), (0.01, 99.99)],
)
def test_withdraw_decreases_balance(account, amount, expected):
    account.withdraw(amount)

    assert account.get_balance() == pytest.approx(expected)


@pytest.mark.parametrize("amount", [0, -10])
def test_withdraw_rejects_non_positive_amount(account, amount):
    with pytest.raises(
        ValueError, match="Withdraw amount must be greater than zero"
    ):
        account.withdraw(amount)


def test_withdraw_rejects_insufficient_funds(account):
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(100.01)

    assert account.balance == 100.0


def test_withdraw_rejects_non_numeric_amount(account):
    with pytest.raises(TypeError, match="Withdraw amount must be a number"):
        account.withdraw(None)


@pytest.mark.parametrize(
    ("percent", "expected"),
    [(0, 100.0), (10, 110.0), (2.5, 102.5), (100, 200.0)],
)
def test_add_interest_increases_balance(account, percent, expected):
    account.add_interest(percent)

    assert account.get_balance() == pytest.approx(expected)


def test_add_interest_rejects_invalid_percent(account):
    with pytest.raises(ValueError, match="Interest percent cannot be negative"):
        account.add_interest(-1)

    with pytest.raises(TypeError, match="Interest percent must be a number"):
        account.add_interest("5")


def test_operations_sequence_gives_expected_balance(account):
    account.deposit(100)  # 200
    account.withdraw(50)  # 150
    account.add_interest(10)  # 165

    assert account.get_balance() == pytest.approx(165.0)


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Example conditional skip: demonstrates skipif on platform",
)
def test_get_balance_returns_float(account):
    assert isinstance(account.get_balance(), float)


@pytest.mark.xfail(
    reason="BankAccount does not round balance to 2 decimals (known limitation)",
    strict=True,
)
def test_balance_is_rounded_after_interest():
    acc = BankAccount("Ivan", 10)
    acc.add_interest(3.333)

    assert acc.get_balance() == round(acc.get_balance(), 2)
