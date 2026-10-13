from customer import Customer
from payment import Payment
from rental import Rental
import uuid
from vehicle import EconomyCar, LuxuryCar, SUV, Vehicle


class CarRentalSystem:
    """Central business operations engine managing entities, rules, and revenue."""

    def __init__(self, name: str = "SafariDrive Rentals"):
        self.name = name
        self.vehicles = []
        self.customers = []
        self.rentals = []
        self.payments = []
        self.__revenue = 0.0  # Encapsulated private business revenue

    @property
    def revenue(self) -> float:
        """Read-only access to accumulated business revenue."""
        return self.__revenue

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """Adds a new vehicle to the fleet with uniqueness check."""
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Only instances of Vehicle subclasses can be added.")
        if self.find_vehicle(vehicle.registration_number):
            raise ValueError(f"Vehicle with registration {vehicle.registration_number} already exists.")
        self.vehicles.append(vehicle)

    def register_customer(self, customer: Customer) -> None:
        """Registers a customer if ID is unique."""
        if not isinstance(customer, Customer):
            raise TypeError("Only Customer instances can be registered.")
        if self.find_customer(customer.customer_id):
            raise ValueError(f"Customer with ID {customer.customer_id} already exists.")
        self.customers.append(customer)

    def find_vehicle(self, registration_number: str):
        """Finds vehicle by registration string, or returns None."""
        clean_reg = registration_number.strip().upper()
        for v in self.vehicles:
            if v.registration_number == clean_reg:
                return v
        return None

    def find_customer(self, customer_id: str):
        """Finds registered customer by ID, or returns None."""
        clean_id = customer_id.strip()
        for c in self.customers:
            if c.customer_id == clean_id:
                return c
        return None

    def find_rental(self, rental_id: str):
        """Finds rental by ID, or returns None."""
        clean_id = rental_id.strip().upper()
        for r in self.rentals:
            if r.rental_id.upper() == clean_id:
                return r
        return None

    def show_available_vehicles(self) -> None:
        """Lists all currently available vehicles."""
        availables = [v for v in self.vehicles if v.is_available()]
        print(f"\n--- AVAILABLE FLEET ({len(availables)} vehicles) ---")
        if not availables:
            print("No vehicles are currently available.")
            return
        for idx, v in enumerate(availables, 1):
            print(f"{idx}. {v.make} {v.model} ({v.registration_number}) - KSh {v.daily_rate:,.0f}/day [{v.__class__.__name__}]")

    def search_vehicles(self, vehicle_type: str | None = None, max_daily_rate: float | None = None):
        """Filters available vehicles by subclass name and/or maximum daily budget."""
        results = [v for v in self.vehicles if v.is_available()]

        if vehicle_type:
            results = [v for v in results if v.__class__.__name__.lower() == vehicle_type.strip().lower()]
        if max_daily_rate is not None:
            results = [v for v in results if v.daily_rate <= max_daily_rate]

        title = f"AVAILABLE {vehicle_type.upper()}s" if vehicle_type else "AVAILABLE VEHICLES"
        print(f"\n{title}\n")
        if not results:
            print("No vehicles matched your search criteria.")
            return results

        for idx, car in enumerate(results, 1):
            print(f"{idx}. {car.make} {car.model}")
            print(f"   Registration: {car.registration_number}")
            print(f"   Rate: KSh {car.daily_rate:,.0f}/day\n")
        return results

    def rent_vehicle(self, customer: Customer, vehicle: Vehicle, days: int, rental_id: str | None = None) -> Rental:
        """Enforces prerequisite rules, creates a Rental record, and updates vehicle status."""
        if customer not in self.customers:
            raise ValueError("A customer must be registered before renting.")
        if vehicle not in self.vehicles:
            raise ValueError("A vehicle must be in the fleet before it is rented.")
        if not vehicle.is_available():
            raise ValueError("A rented vehicle cannot be rented again.")
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")

        # Fallback to a generated string ID if rental_id is None
        active_id = rental_id or str(uuid.uuid4())

        # Pass the guaranteed string to the constructor
        rental = Rental(rental_id=active_id, customer=customer, vehicle=vehicle, rental_days=days)
        
        vehicle.mark_as_rented()
        customer.add_rental(rental)
        self.rentals.append(rental)
        return rental


    def return_vehicle(self, rental: Rental, actual_days: int, damage_charge: float = 0.0) -> None:
        """Processes the return of an active rental and frees the vehicle."""
        if rental not in self.rentals:
            raise ValueError("Rental record not found in system.")
        if rental.vehicle.is_available() and rental.status != "ACTIVE":
            raise ValueError("A vehicle cannot be returned unless it is currently rented.")

        rental.complete_rental(actual_days=actual_days, damage_charge=damage_charge)
        rental.vehicle.mark_as_available()

    def process_payment(self, payment: Payment) -> bool:
        """
        Validates business rules for settling rental payments:
        Must be completed, not already paid, and only updates revenue on success.
        """
        if not isinstance(payment, Payment):
            raise TypeError("Invalid payment object.")

        rental = payment.rental
        if rental.status != "COMPLETED":
            raise ValueError("A rental can only be paid once, and only after it is completed.")
        if rental.is_paid():
            raise ValueError("A rental can only be paid once, and only after it is completed.")

        success = payment.process_payment()
        if success:
            rental.mark_as_paid()
            self.__revenue += payment.amount  # Controlled mutation of private revenue
            self.payments.append(payment)
            return True
        return False

    def show_active_rentals(self) -> None:
        """Lists all ongoing rentals."""
        actives = [r for r in self.rentals if r.status == "ACTIVE"]
        print(f"\n--- ACTIVE RENTALS ({len(actives)}) ---")
        if not actives:
            print("No rentals currently active.")
            return
        for r in actives:
            print(
                f"- ID: {r.rental_id} | Customer: {r.customer.name} | "
                f"Vehicle: {r.vehicle.make} {r.vehicle.model} ({r.vehicle.registration_number}) | "
                f"Days Booked: {r.rental_days} | Base: KSh {r.base_cost:,.0f}"
            )

    def show_completed_rentals(self) -> None:
        """Lists all completed rentals."""
        completed = [r for r in self.rentals if r.status == "COMPLETED"]
        print(f"\n--- COMPLETED RENTALS ({len(completed)}) ---")
        if not completed:
            print("No rentals completed yet.")
            return
        for r in completed:
            paid_str = "PAID" if r.is_paid() else "PENDING PAYMENT"
            print(
                f"- ID: {r.rental_id} | Customer: {r.customer.name} | "
                f"Vehicle: {r.vehicle.registration_number} | "
                f"Final Bill: KSh {r.calculate_total():,.0f} | Status: {paid_str}"
            )

    def generate_report(self) -> None:
        """Calculates live analytics across all entity collections and prints management metrics."""
        total_vehicles = len(self.vehicles)
        available_vehicles = sum(1 for v in self.vehicles if v.is_available())
        rented_vehicles = total_vehicles - available_vehicles

        total_customers = len(self.customers)

        total_rentals = len(self.rentals)
        active_rentals = sum(1 for r in self.rentals if r.status == "ACTIVE")
        completed_rentals = sum(1 for r in self.rentals if r.status == "COMPLETED")

        economy_count = sum(1 for v in self.vehicles if isinstance(v, EconomyCar))
        suv_count = sum(1 for v in self.vehicles if isinstance(v, SUV))
        luxury_count = sum(1 for v in self.vehicles if isinstance(v, LuxuryCar))

        print("\n=====================================")
        print("    SAFARIDRIVE MANAGEMENT REPORT    ")
        print("=====================================")
        print(f"Total Vehicles:              {total_vehicles:>2}")
        print(f"Available Vehicles:          {available_vehicles:>2}")
        print(f"Rented Vehicles:             {rented_vehicles:>2}\n")
        print(f"Registered Customers:        {total_customers:>2}\n")
        print(f"Total Rentals:               {total_rentals:>2}")
        print(f"Active Rentals:              {active_rentals:>2}")
        print(f"Completed Rentals:           {completed_rentals:>2}\n")
        print(f"Total Revenue:      KSh {self.revenue:>9,.0f}")
        print("-------------------------------------")
        print("VEHICLES BY CATEGORY")
        print(f"Economy Cars:                {economy_count:>2}")
        print(f"SUVs:                        {suv_count:>2}")
        print(f"Luxury Cars:                 {luxury_count:>2}")
        print("=====================================\n")