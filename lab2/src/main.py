
import re


class EmailValidationError(ValueError):
    pass


class PasswordValidationError(ValueError):
    pass


class AgeValidationError(ValueError):
    pass


class UserRegistrationValidator:
    MIN_AGE = 18
    MIN_PASSWORD_LENGTH = 8

    def validate_email(self, email: str) -> bool:
        if not isinstance(email, str):
            raise TypeError("Email must be a string")

        if not email.strip():
            raise EmailValidationError("Email cannot be empty")

        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(pattern, email):
            raise EmailValidationError("Invalid email format")

        return True

    def validate_password(self, password: str) -> bool:
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        if len(password) < self.MIN_PASSWORD_LENGTH:
            raise PasswordValidationError(
                "Password must contain at least 8 characters"
            )

        if not any(char.isupper() for char in password):
            raise PasswordValidationError(
                "Password must contain an uppercase letter"
            )

        if not any(char.islower() for char in password):
            raise PasswordValidationError(
                "Password must contain a lowercase letter"
            )

        if not any(char.isdigit() for char in password):
            raise PasswordValidationError(
                "Password must contain a digit"
            )

        return True

    def validate_age(self, age: int) -> bool:
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")

        if age < 0:
            raise AgeValidationError("Age cannot be negative")

        if age < self.MIN_AGE:
            raise AgeValidationError(
                "User must be at least 18 years old"
            )

        return True

    def validate_user(
        self,
        email: str,
        password: str,
        age: int,
    ) -> bool:
        self.validate_email(email)
        self.validate_password(password)
        self.validate_age(age)

        return True

