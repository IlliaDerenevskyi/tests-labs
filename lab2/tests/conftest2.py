import pytest

from src.main2 import BankAccount


@pytest.fixture
def account():
    test_account = BankAccount("Ivan", 100)
    yield test_account
    test_account.__dict__.clear()
