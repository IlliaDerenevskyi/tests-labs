from src.bank_account import BankAccount


def test_deposit_adds_money():
    account = BankAccount()
    account.deposit(100)

    assert account.get_balance() == 100