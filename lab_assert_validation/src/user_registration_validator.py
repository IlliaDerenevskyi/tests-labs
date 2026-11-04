class UserRegistrationValidator:
    def validate_email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        if "@" not in email or not email.split("@")[-1]:
            raise ValueError("Email is invalid")
        return True

    def validate_password(self, password):
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain a digit")
        return True

    def validate_age(self, age):
        if not isinstance(age, int) or isinstance(age, bool):
            raise TypeError("Age must be an integer")
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120")
        return True

    def validate(self, email, password, age):
        self.validate_email(email)
        self.validate_password(password)
        self.validate_age(age)
        return True
