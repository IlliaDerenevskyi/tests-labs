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
