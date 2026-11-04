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
