# RentFlow

RentFlow is a Python-based vehicle rental management system for a car rental business. It models the core operations of a rental company, including vehicle inventory management, customer registration, rental transactions, payment processing, and business reporting.

The project is designed to simulate a realistic rental workflow with strong validation and structured classes for each domain concept.

## Features

- Vehicle fleet management
  - Add economy, SUV, and luxury vehicles
  - Track vehicle availability and rental status
  - Search and filter available vehicles by category and daily rate
- Customer management
  - Register customers with personal details
  - Track each customer's rental history
- Rental lifecycle management
  - Create active rentals
  - Complete rentals after return
  - Apply late fees and damage charges
  - Cancel active rentals when needed
- Payment handling
  - M-Pesa, card, and cash payment simulation
  - Payment validation and transaction logging
- Reporting
  - Management summary report with vehicle fleet stats, completed rentals, and total revenue

## Project Structure

```text
RentFlow/
├── customer.py
├── main.py
├── payment.py
├── rental.py
├── rental_system.py
├── vehicle.py
└── README.md
```

## Main Classes

- `Vehicle` - abstract base class for all rental vehicles
- `EconomyCar` - economy-class vehicle type
- `SUV` - SUV vehicle with service charge
- `LuxuryCar` - luxury vehicle with insurance surcharge
- `Customer` - registered renter details and rental history
- `Rental` - billing, status, and lifecycle management for a rental agreement
- `Payment` - abstract payment interface
- `MpesaPayment`, `CardPayment`, `CashPayment` - concrete payment methods
- `CarRentalSystem` - orchestrates the rental operations and reporting

## Requirements

This project uses only the Python standard library. No external dependencies are required.

## How to Run

From the project directory, run:

```bash
python main.py
```

This launches the specification walkthrough demo and then opens the interactive terminal menu for manual rental operations.

## Example Workflow

1. Add vehicles to the fleet
2. Register customers
3. Rent a vehicle for a number of days
4. Return the vehicle after the actual rental period
5. Process payment using a supported method
6. View active/completed rentals and management report

## Notes

- Vehicle and customer lookups are case-insensitive for identifiers and vehicle registration strings.
- Business rules prevent invalid actions like renting an already rented vehicle or paying before a rental is completed.
- The system includes example values for SafariDrive Rentals, such as Kenyan mobile phone validation and local pricing logic.

## License

This project is provided for educational and demonstration purposes.
