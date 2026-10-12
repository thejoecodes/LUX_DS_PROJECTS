class Customer:
    """Represents a rental customer registered in the system."""

    def __init__(self, customer_id: str, name: str, phone_number: str, national_id: str, driving_licence: str):
        if not driving_licence or not driving_licence.strip():
            raise ValueError("A customer must have a valid driving licence.")
        if not name or not name.strip():
            raise ValueError("Customer name cannot be empty.")

        self.customer_id = customer_id.strip()
        self.name = name.strip()
        self.phone_number = phone_number.strip()
        self.national_id = national_id.strip()
        self.driving_licence = driving_licence.strip()
        self.rentals = []

    def add_rental(self, rental) -> None:
        """Appends a new rental record to the customer's personal history."""
        self.rentals.append(rental)

    def display_details(self) -> None:
        """Prints customer profile details."""
        print(
            f"Customer ID: {self.customer_id} | Name: {self.name} | "
            f"Phone: {self.phone_number} | DL: {self.driving_licence} | Total Rentals: {len(self.rentals)}"
        )

    def view_rental_history(self) -> None:
        """Prints an itemized summary of all rentals undertaken by this customer."""
        print(f"\n--- Rental History for {self.name} ({self.customer_id}) ---")
        if not self.rentals:
            print("No rental transactions found.")
            return

        for r in self.rentals:
            print(
                f"- [{r.rental_id}] {r.vehicle.make} {r.vehicle.model} ({r.vehicle.registration_number}) | "
                f"Status: {r.status} | Total: KSh {r.calculate_total():,.2f} | Paid: {r.is_paid()}"
            )