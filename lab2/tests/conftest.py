import pytest

from src.main import UserRegistrationValidator


@pytest.fixture
def validator():
    test_validator = UserRegistrationValidator()
    yield test_validator
    test_validator.__dict__.clear()
