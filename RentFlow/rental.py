from vehicle import SUV, LuxuryCar


class Rental:
    """Manages the lifecycle, billing calculations, and status of a rental contract."""

    _rental_counter = 1

    def __init__(self, rental_id: str, customer, vehicle, rental_days: int):
        if rental_days <= 0:
            raise ValueError("Rental days must be greater than zero.")

        self.rental_id = rental_id if rental_id else f"R{Rental._rental_counter:03d}"
        Rental._rental_counter += 1

        self.customer = customer
        self.vehicle = vehicle
        self.rental_days = int(rental_days)
        self.actual_days = None
        self.status = "ACTIVE"  # Lifecycle: ACTIVE -> COMPLETED (or CANCELLED)

        # Base billing breakdown
        self.base_cost = self.vehicle.calculate_rental_cost(self.rental_days)
        self.late_fee = 0.0
        self.damage_charge = 0.0
        self.__paid = False  # Encapsulated private payment flag

    def is_paid(self) -> bool:
        """Returns True if the invoice for this rental has been settled."""
        return self.__paid

    def mark_as_paid(self) -> None:
        """Marks the rental invoice as settled."""
        self.__paid = True

    def calculate_late_fee(self) -> float:
        """
        Calculates penalty for late return:
        Daily late penalty = 20% of vehicle daily rate
        Late fee = daily penalty * late days (only for positive late days)
        """
        if self.actual_days is None or self.actual_days <= self.rental_days:
            return 0.0
        late_days = self.actual_days - self.rental_days
        daily_penalty = 0.20 * self.vehicle.daily_rate
        return daily_penalty * late_days

    def calculate_total(self) -> float:
        """Returns base_cost + late_fee + damage_charge."""
        return self.base_cost + self.late_fee + self.damage_charge

    def complete_rental(self, actual_days: int, damage_charge: float = 0.0) -> None:
        """Records return metrics, computes late fees and damages, and marks rental COMPLETED."""
        if self.status == "COMPLETED":
            raise ValueError("A completed rental cannot be completed again.")
        if self.status == "CANCELLED":
            raise ValueError("A cancelled rental cannot be completed.")
        if actual_days <= 0:
            raise ValueError("Actual days kept must be at least 1.")
        if damage_charge < 0:
            raise ValueError("Damage charge cannot be negative.")

        self.actual_days = int(actual_days)
        self.damage_charge = float(damage_charge)
        self.late_fee = self.calculate_late_fee()
        self.status = "COMPLETED"

    def cancel_rental(self) -> None:
        """Cancels an active rental before return."""
        if self.status != "ACTIVE":
            raise ValueError("Only ACTIVE rentals can be cancelled.")
        self.status = "CANCELLED"
        self.vehicle.mark_as_available()

    def display_rental_details(self) -> None:
        """Renders the official rental receipt matching specification layout."""
        subtotal = self.vehicle.daily_rate * self.rental_days

        print("====================================")
        print("        SAFARIDRIVE RENTALS         ")
        print("====================================")
        print(f"Rental ID:        {self.rental_id}")
        print(f"Customer:         {self.customer.name}")
        print(f"Vehicle:          {self.vehicle.make} {self.vehicle.model}")
        print(f"Registration:     {self.vehicle.registration_number}")
        print(f"Rental Period:    {self.rental_days} days")
        print(f"Daily Rate:       KSh {self.vehicle.daily_rate:,.0f}")
        print()
        print(f"Rental Charge:    KSh {subtotal:,.0f}")

        # Type-specific billing lines
        if isinstance(self.vehicle, SUV):
            print(f"Service Charge:   KSh {self.vehicle.SERVICE_CHARGE:,.0f}")
        elif isinstance(self.vehicle, LuxuryCar):
            insurance_amt = subtotal * self.vehicle.INSURANCE_RATE
            print(f"Insurance (10%):  KSh {insurance_amt:,.0f}")

        if self.late_fee > 0:
            print(f"Late Fee:         KSh {self.late_fee:,.0f}")
        if self.damage_charge > 0:
            print(f"Damage Charge:    KSh {self.damage_charge:,.0f}")

        print("------------------------------------")
        print(f"TOTAL:            KSh {self.calculate_total():,.0f}")
        print(f"Status:           {self.status}")
        print(f"Payment Status:   {'PAID' if self.__paid else 'UNPAID'}")
        print("====================================")