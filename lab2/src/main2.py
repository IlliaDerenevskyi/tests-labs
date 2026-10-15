class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        if not isinstance(owner, str):
            raise TypeError("Owner must be a string")

        if not owner.strip():
            raise ValueError("Owner name cannot be empty")

        if not isinstance(balance, (int, float)):
            raise TypeError("Balance must be a number")

        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.owner = owner
        self.balance = float(balance)

    def deposit(self, amount: float):
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be a number")

        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero")

        self.balance += amount

    def withdraw(self, amount: float):
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdraw amount must be a number")

        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than zero")

        if amount > self.balance:
            raise ValueError("Insufficient funds")

        self.balance -= amount

    def add_interest(self, percent: float):
        if not isinstance(percent, (int, float)):
            raise TypeError("Interest percent must be a number")

        if percent < 0:
            raise ValueError("Interest percent cannot be negative")

        interest = self.balance * percent / 100
        self.balance += interest

    def get_balance(self) -> float:
        return self.balance

