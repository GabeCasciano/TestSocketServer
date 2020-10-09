from .Employee import Employee
from .Person import Person
from .Client import Client
from .Schedule import Appointment, Schedule

from datetime import datetime
import csv

class Company:

    def __init__(self, name: str):
        self.name = name
        self.employees = []
        self.clients = []
        self.org_number = 1

    def add_employee(self, name: str = None, age: int = None, emp: Person = None):
        if emp != None:
            for e in self.employees:
                if e.organization_number == emp.organization_number:
                    return False
            self.employees.append(emp)
        else:
            emp = Employee(name, age, self.org_number)
            self.org_number += 1
            self.employees.append(emp)

    def add_customer(self, name: str = None, age: int = None, cust: Person = None):
        if cust != None:
            for c in self.clients:
                if c.organization_number == cust.organization_number:
                    return False
            self.clients.append(cust)
        else:
            cust = Client(name, age, self.org_number)
            self.org_number += 1
            self.employees.append(cust)

    def book_employee(self,  date: datetime, employee: Employee, client: Client):
        for e in self.employees:
            if e.organization_number == employee.organization_number:
                e.book(date, client)
                break

    def toggle_location(self, person: Person):
        for e in self.employees:
            if e.organization_number == person.organization_number:
                if e.present == False:
                    e.check_in()
                else:
                    e.check_out()
                return
        for c in self.clients:
            if c.organization_number == person.organization_number:
                if e.present == False:
                    e.check_in()
                else:
                    e.check_out()
                return

    def get_info(self):
        emp = []
        cust = []
        for e in self.employees:
            emp.append(e.format_csv())
        for c in self.clients:
            cust.append(c.format_csv())

        return emp, cust

    def get_person_info(self, name: str = None, number: int = None):
        if number != None:
            for e in self.employees:
                if e.organization_number == number:
                    return e
            for c in self.clients:
                if c.organization_number == number:
                    return c
        if name != None:
            for e in self.employees:
                if e.name == name:
                    return e
            for c in self.clients:
                if c.name == name:
                    return c
        return None

    def save(self):
        with open("Data/employees.csv", "w") as file:
            for e in self.employees:
                file.write(e.format_csv_w_sch())

        with open("Data/customers.csv", "w") as file:
            for c in self.clients:
                file.write(c.format_csv_w_sch())

    def load(self):
        with open("Data/employees.csv", "r", newline='') as file:
            reader = csv.reader(file, delimiter=",")

            for row in reader:
                if row[1] > self.org_number:
                    self.org_number = row[1]

                e = Employee(row[1], row[2], row[0])
                sch = row[4].split(";")
                for s in sch:
                    d = s.split(":")
                    if d.__len__() > 0:
                        e.sch.book_apt(datetime.strptime(d[0], '%c'), d[1], d[2])

        with open("Data/customers.csv", "r", newline='') as file:
            reader = csv.reader(file, delimiter=",")

            for row in reader:
                if row[1] > self.org_number:
                    self.org_number = row[1]

                c = Client(row[1], row[2], row[0])
                sch = row[4].split(";")
                for s in sch:
                    d = s.split(":")
                    if d.__len__() > 0:
                        c.sch.book_apt(datetime.strptime(d[0], '%c'), d[1], d[2])
