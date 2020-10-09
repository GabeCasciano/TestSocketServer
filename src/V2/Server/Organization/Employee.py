from .Person import Person
from .Schedule import Appointment, Schedule

from datetime import datetime


class Employee(Person):
    def __init__(self, name: str = None, age: int = None, organization_number: int = None):
        Person.__init__(name, age, organization_number)

    def book(self, date: datetime, customer: Person):
        if self.organization_number != customer.organization_number:
            apt = self.schd.book_apt(date, self.organization_number, customer.organization_number)
            customer.book_apt(apt=apt)
