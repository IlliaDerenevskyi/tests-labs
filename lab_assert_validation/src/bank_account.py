class BankAccount:
    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._balance = initial_balance

    @staticmethod
    def _validate_positive_amount(amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def deposit(self, amount):
        self._validate_positive_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        self._validate_positive_amount(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def get_balance(self):
        return self._balance
