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
