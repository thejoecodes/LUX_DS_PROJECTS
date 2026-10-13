from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Abstract base class representing a generic vehicle in the fleet."""

    def __init__(self, registration_number: str, make: str, model: str, year: int, daily_rate: float):
        if daily_rate < 0:
            raise ValueError("Daily rate cannot be negative.")

        self.registration_number = registration_number.strip().upper()
        self.make = make.strip()
        self.model = model.strip()
        self.year = year
        self.daily_rate = float(daily_rate)
        self.__available = True  # Encapsulated private attribute

    def is_available(self) -> bool:
        """Returns True if the vehicle is currently available for rent."""
        return self.__available

    def mark_as_rented(self) -> None:
        """Marks the vehicle as rented (unavailable)."""
        self.__available = False

    def mark_as_available(self) -> None:
        """Marks the vehicle as returned (available)."""
        self.__available = True

    def display_details(self) -> None:
        """Displays formatted specifications and current availability."""
        status = "Available" if self.__available else "Rented"
        print(
            f"[{self.__class__.__name__}] {self.year} {self.make} {self.model} "
            f"({self.registration_number}) - Rate: KSh {self.daily_rate:,.2f}/day | Status: {status}"
        )

    @abstractmethod
    def calculate_rental_cost(self, days: int) -> float:
        """Abstract method implemented by subclasses with specific pricing formulas."""
        pass


class EconomyCar(Vehicle):
    """Economy segment: Standard daily rate with no mandatory add-ons."""

    def __init__(self, registration_number: str, make: str, model: str, year: int, daily_rate: float):
        super().__init__(registration_number, make, model, year, daily_rate)

    def calculate_rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")
        return self.daily_rate * days


class SUV(Vehicle):
    """SUV segment: Standard daily rate plus a one-time KSh 2,000 service surcharge."""

    SERVICE_CHARGE = 2000.0

    def __init__(self, registration_number: str, make: str, model: str, year: int, daily_rate: float):
        super().__init__(registration_number, make, model, year, daily_rate)

    def calculate_rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")
        return (self.daily_rate * days) + self.SERVICE_CHARGE


class LuxuryCar(Vehicle):
    """Luxury segment: Standard daily rate plus a 10% comprehensive insurance premium."""

    INSURANCE_RATE = 0.10

    def __init__(self, registration_number: str, make: str, model: str, year: int, daily_rate: float):
        super().__init__(registration_number, make, model, year, daily_rate)

    def calculate_rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")
        subtotal = self.daily_rate * days
        return subtotal + (subtotal * self.INSURANCE_RATE)

    axio = EconomyCar("KDK 123A", "Toyota", "Axio", 2020, 3000.0)
    axio.display_details()
    print(axio.calculate_rental_cost(5))  # Example usage