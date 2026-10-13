import random
import re
import string
from abc import ABC, abstractmethod


class Payment(ABC):
    """Abstract base class handling payment processing for completed rentals."""

    def __init__(self, rental):
        if rental.calculate_total() < 0:
            raise ValueError("Payment amounts cannot be negative.")

        self.rental = rental
        self.amount = rental.calculate_total()

    @abstractmethod
    def process_payment(self) -> bool:
        """Abstract payment processing method returning True on success, False on failure."""
        pass


class MpesaPayment(Payment):
    """M-Pesa payment gateway implementation."""

    def __init__(self, rental, phone_number: str):
        super().__init__(rental)
        if phone_number.startswith('+254'):
            phone_number = '0' + phone_number[4:] # Convert to local format
        if not re.match(r"^(07|01)\d{8}$", phone_number):
            raise ValueError("Invalid Kenyan phone number format. Must start with 07 or 01 and be 10 digits long.")
        if not phone_number or len(phone_number.strip()) < 10:
            raise ValueError("A valid Kenyan phone number is required for M-Pesa payments.")
        self.phone_number = phone_number.strip()
        self.transaction_code = None

    def _generate_transaction_code(self) -> str:
        prefix = "".join(random.choices(string.ascii_uppercase, k=3))
        digits = "".join(random.choices(string.digits, k=2))
        suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"{prefix}{digits}{suffix}"

    def process_payment(self) -> bool:
        self.transaction_code = self._generate_transaction_code()
        print("Processing M-Pesa payment...")
        print(f"Transaction: {self.transaction_code}")
        print(f"Payment of KSh {self.amount:,.0f} successful.")
        return True


class CardPayment(Payment):
    """Card processing simulation retaining only PCI-compliant last 4 digits."""

    def __init__(self, rental, card_last_four: str):
        super().__init__(rental)
        cleaned = card_last_four.strip()
        if len(cleaned) != 4 or not cleaned.isdigit():
            raise ValueError("Card last four digits must be exactly 4 numeric characters.")
        self.card_last_four = cleaned

    def process_payment(self) -> bool:
        print("Processing Card payment...")
        print(f"Card ending {self.card_last_four} charged KSh {self.amount:,.0f}.")
        return True


class CashPayment(Payment):
    """Cash transaction handler validating tender amount and dispensing change."""

    def __init__(self, rental, cash_tendered: float):
        super().__init__(rental)
        if cash_tendered < 0:
            raise ValueError("Cash tendered cannot be negative.")
        self.cash_tendered = float(cash_tendered)

    def process_payment(self) -> bool:
        print("Processing Cash payment...")
        if self.cash_tendered < self.amount:
            shortage = self.amount - self.cash_tendered
            print(f"Payment failed: Cash tendered is short by KSh {shortage:,.2f}.")
            return False

        change = self.cash_tendered - self.amount
        print(f"Cash received: KSh {self.cash_tendered:,.0f}")
        print(f"Change due:    KSh {change:,.0f}")
        print(f"Cash payment of KSh {self.amount:,.0f} recorded.")
        return True