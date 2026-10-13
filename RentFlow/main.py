from customer import Customer
from payment import CardPayment, CashPayment, MpesaPayment
from rental_system import CarRentalSystem
from vehicle import EconomyCar, LuxuryCar, SUV


def run_spec_walkthrough():
    """Executes the test suite and workflow scenario from the requirements brief."""
    print("\n--- RUNNING SPECIFICATION WALKTHROUGH DEMO ---")
    system = CarRentalSystem("SafariDrive Rentals")

    # 1. Add vehicles
    car1 = EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000)
    car2 = SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000)
    car3 = SUV("KDJ 672B", "Nissan", "X-Trail", 2021, 6500)
    car4 = LuxuryCar("KDL 789C", "Mercedes-Benz", "E-Class", 2024, 15000)
    car5= EconomyCar("KDE 948A", "Nissan", "Note", 2022, 4000)

    for car in [car1, car2, car3, car4, car5]:
        system.add_vehicle(car)

    # 2. Register a customer
    customer1 = Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821")
    customer2 = Customer("C002", "Jane Mwangi", "0712345679", "12345679", "DL45822")
    customer3 = Customer("C003", "Peter Otieno", "0712345680", "12345680", "DL45823")
    system.register_customer(customer1)
    system.register_customer(customer2)
    system.register_customer(customer3)

    # 3. Rent the Prado for 4 days
    system.show_available_vehicles()
    rental1 = system.rent_vehicle(customer1, car1, 4, rental_id="R001")
    rental1.display_rental_details()

    # 4. Try to rent it again (should fail)
    try:
        system.rent_vehicle(customer1, car2, 2)
    except ValueError as error:
        print(f"\nCaught Expected Error: {error}")

    # 5. Return it 2 days late (actual_days=6), then pay with M-Pesa
    print("\nProcessing Return (2 days late)...")
    system.return_vehicle(rental1, actual_days=6)

    payment1 = MpesaPayment(rental1, "0712345678")
    system.process_payment(payment1)

    # 6. Generate Management Report
    system.generate_report()


def interactive_menu():
    """Terminal menu interface for live manual operation."""
    system = CarRentalSystem("SafariDrive Rentals")

    # Seed initial fleet & customers
    system.add_vehicle(EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000))
    system.add_vehicle(SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000))
    system.add_vehicle(SUV("KDJ 672B", "Nissan", "X-Trail", 2021, 6500))
    system.add_vehicle(LuxuryCar("KDL 789C", "Mercedes-Benz", "E-Class", 2024, 15000))
    system.register_customer(Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821"))

    while True:
        print("\n================================")
        print("      SAFARIDRIVE RENTALS       ")
        print("================================")
        print("1. Register Customer")
        print("2. Add Vehicle")
        print("3. View Available Vehicles")
        print("4. Rent Vehicle")
        print("5. Return Vehicle")
        print("6. Process Payment")
        print("7. View Active Rentals")
        print("8. View Completed Rentals")
        print("9. Generate Management Report")
        print("10. Exit")

        choice = input("\nChoose an option (1-10): ").strip()

        try:
            if choice == "1":
                cid = input("Customer ID (e.g. C002): ").strip()
                name = input("Full Name: ").strip()
                phone = input("Phone Number: ").strip()
                if not phone.isdigit():
                    print("Invalid phone number. Please enter a valid phone number.")
                    continue
                nat_id = input("National ID: ").strip()
                if not nat_id.isdigit():
                    print("Invalid national ID. Please enter a valid national ID.")
                    continue
                dl = input("Driving Licence: ").strip()
                system.register_customer(Customer(cid, name, phone, nat_id, dl))
                print(f"Customer {name} registered successfully.")

            elif choice == "2":
                print("Types: 1. Economy | 2. SUV | 3. Luxury")
                t_choice = input("Select type (1-3): ").strip()
                reg = input("Registration (e.g. KDA 001A): ").strip()
                make = input("Make: ").strip()
                model = input("Model: ").strip()
                year = int(input("Year: ").strip())
                rate = float(input("Daily Rate (KSh): ").strip())

                if t_choice == "1":
                    system.add_vehicle(EconomyCar(reg, make, model, year, rate))
                elif t_choice == "2":
                    system.add_vehicle(SUV(reg, make, model, year, rate))
                elif t_choice == "3":
                    system.add_vehicle(LuxuryCar(reg, make, model, year, rate))
                else:
                    print("Invalid category selected.")
                    continue
                print("Vehicle added to fleet.")

            elif choice == "3":
                system.show_available_vehicles()

            elif choice == "4":
                cid = input("Enter Customer ID: ").strip()
                cust = system.find_customer(cid)
                if not cust:
                    raise ValueError(f"Customer {cid} not registered.")

                reg = input("Enter Vehicle Registration: ").strip()
                veh = system.find_vehicle(reg)
                if not veh:
                    raise ValueError(f"Vehicle {reg} not found in fleet.")

                days = int(input("Rental Days: ").strip())
                rental = system.rent_vehicle(cust, veh, days)
                rental.display_rental_details()

            elif choice == "5":
                rid = input("Enter Rental ID to return: ").strip()
                rental = system.find_rental(rid)
                if not rental:
                    raise ValueError(f"Rental {rid} not found.")

                actual = int(input("Actual Days Kept: ").strip())
                dmg = float(input("Damage Charges (0 if none): ") or 0)
                system.return_vehicle(rental, actual, dmg)
                print(f"Vehicle returned. Total bill is KSh {rental.calculate_total():,.0f}.")
                rental.display_rental_details()

            elif choice == "6":
                rid = input("Enter Rental ID to pay for: ").strip()
                rental = system.find_rental(rid)
                if not rental:
                    raise ValueError(f"Rental {rid} not found.")

                print("Payment Methods: 1. M-Pesa | 2. Card | 3. Cash")
                pm = input("Select Method (1-3): ").strip()
                if pm == "1":
                    phone = input("Phone Number: ").strip()
                    pay_obj = MpesaPayment(rental, phone)
                elif pm == "2":
                    last4 = input("Last 4 digits of card: ").strip()
                    pay_obj = CardPayment(rental, last4)
                elif pm == "3":
                    cash = float(input("Cash Tendered: ").strip())
                    pay_obj = CashPayment(rental, cash)
                else:
                    print("Invalid payment option.")
                    continue

                system.process_payment(pay_obj)

            elif choice == "7":
                system.show_active_rentals()

            elif choice == "8":
                system.show_completed_rentals()

            elif choice == "9":
                system.generate_report()

            elif choice == "10":
                print("Exiting RentFlow. Goodbye!")
                break
            else:
                print("Invalid selection. Choose an option between 1 and 10.")

        except ValueError as err:
            print(f"Error: {err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Runs the exact verification script required by Part 10
    run_spec_walkthrough()

    # Launch interactive terminal UI
    interactive_menu()