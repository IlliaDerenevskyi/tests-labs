import pytest

from src.main import (
    AgeValidationError,
    EmailValidationError,
    PasswordValidationError,
)


def test_validate_email_accepts_valid_addresses(validator):
    assert validator.validate_email("student@example.com") is True
    assert validator.validate_email("first.last+lab@university.edu") is True


@pytest.mark.parametrize(
    "email",
    [
        "plainaddress",
        "student@",
        "student@example",
    ],
)
def test_validate_email_rejects_invalid_formats(validator, email):
    with pytest.raises(EmailValidationError, match="Invalid email format"):
        validator.validate_email(email)


def test_validate_email_rejects_empty_and_non_string_values(validator):
    with pytest.raises(EmailValidationError, match="Email cannot be empty"):
        validator.validate_email("   ")

    with pytest.raises(TypeError, match="Email must be a string"):
        validator.validate_email(None)


def test_validate_password_accepts_password_with_all_requirements(validator):
    assert validator.validate_password("Secure123") is True
    assert validator.validate_password("Lab_password9") is True


@pytest.mark.parametrize(
    ("password", "message"),
    [
        ("Aa12345", "Password must contain at least 8 characters"),
        ("secure123", "Password must contain an uppercase letter"),
        ("SECURE123", "Password must contain a lowercase letter"),
        ("SecurePass", "Password must contain a digit"),
    ],
)
def test_validate_password_rejects_missing_requirements(
    validator, password, message
):
    with pytest.raises(PasswordValidationError, match=message):
        validator.validate_password(password)


def test_validate_password_rejects_non_string_values(validator):
    with pytest.raises(TypeError, match="Password must be a string"):
        validator.validate_password(12345678)


@pytest.mark.parametrize("age", [18, 25, 100])
def test_validate_age_accepts_adult_ages(validator, age):
    assert validator.validate_age(age) is True


def test_validate_age_rejects_invalid_values(validator):
    with pytest.raises(TypeError, match="Age must be an integer"):
        validator.validate_age("18")

    with pytest.raises(AgeValidationError, match="Age cannot be negative"):
        validator.validate_age(-1)

    with pytest.raises(
        AgeValidationError, match="User must be at least 18 years old"
    ):
        validator.validate_age(17)


@pytest.mark.skipif(
    not pytest.__version__.startswith("8"),
    reason="The laboratory environment requires pytest 8 for this example",
)
def test_validate_user_accepts_complete_valid_registration(validator):
    assert validator.validate_user(
        "student@example.com", "Secure123", 18
    ) is True


def test_validate_user_propagates_validation_errors(validator):
    with pytest.raises(EmailValidationError, match="Invalid email format"):
        validator.validate_user("invalid-email", "Secure123", 18)

    with pytest.raises(PasswordValidationError, match="Password must contain"):
        validator.validate_user("student@example.com", "weakpass", 18)

    with pytest.raises(
        AgeValidationError, match="User must be at least 18 years old"
    ):
        validator.validate_user("student@example.com", "Secure123", 17)