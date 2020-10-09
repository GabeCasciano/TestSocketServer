from datetime import datetime


class Appointment:
    def __init__(self, date: datetime, employee_number: int, customer_number: int, number: int):
        self.date = date
        self.employee = employee_number
        self.customer = customer_number
        self.completed = False
        self.number = number

    def change_time(self, new_date: datetime):
        if new_date > datetime.datetime.now():
            self.date = new_date

    def complete(self):
        self.completed = True

    def format_csv(self):
        return f"{self.date.strftime('%c')}:{self.employee}:{self.customer}"


class Schedule:

    def __init__(self):
        self.apts = []
        self.next = None

    def book_apt(self, date: datetime = None, employee: int = None, customer: int = None, apt: Appointment = None):
        if apt != None:
            self.apts.append(apt)
        else:
            apt = Appointment(date, employee, customer, self.apts.__len__() + 1)
        self.apts.append(apt)
        return apt

    def format_csv(self):
        out = "0,"
        if self.apts.__len__() > 0:
            out = ""
            for a in self.apts:
                out += f"{a.format_csv()};"

        return out

    def complete_apt(self, apt_number: int):
        for a in self.apts:
            if a.number == apt_number:
                a.complete()

    def format_bytes(self):
        return str.encode(self.format_csv())
