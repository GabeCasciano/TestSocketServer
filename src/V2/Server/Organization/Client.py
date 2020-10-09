from .Person import Person
from .Employee import Employee
from .Schedule import Appointment, Schedule

from datetime import datetime


class Client(Person):
    def __init__(self, name: str = None, age: int = None, organization_number: int = None):
        Person.__init__(name, age, organization_number)

    def book(self, date: datetime, employee: Employee):
        employee.book(date, self)

