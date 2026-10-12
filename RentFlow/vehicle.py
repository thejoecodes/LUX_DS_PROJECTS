from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, registration_number, make, model, year, daily_rate):
        if daily_rate < 0:
            raise ValueError("Daily rate cannot be negative.")

        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.__available = True          # private

    def is_available(self):
        return self.__available

    def mark_as_rented(self):
        self.__available = False

    def mark_as_available(self):
        self.__available = True

    @abstractmethod
    def calculate_rental_cost(self, days):
        pass

class EconomyCar(Vehicle):
    def calculate_rental_cost(self, days):
        return self.daily_rate * days

class SUV(Vehicle):
    def calculate_rental_cost(self, days):
        return self.daily_rate * days + 2000  # SUVs have a Ksh. 2000 surcharge

class LuxuryCar(Vehicle):
    def calculate_rental_cost(self, days):
        return self.daily_rate * days * 1.1  # Luxury cars have a 10% surcharge