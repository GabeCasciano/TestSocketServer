from .Schedule import Schedule, Appointment

class Person:

    def __init__(self, name: str = None, age: int = None, organization_number: int = None):
        self.name = name
        self.age = age
        self.organization_number = organization_number
        if self.organization_number is None:
            self.organization_number = -1
        self.present = 0
        self.sch = Schedule()

    def set_organization_number(self, num: int):
        self.organization_number = num

    def check_in(self):
        self.present = True

    def check_out(self):
        self.present = False

    def get_schedule(self):
        return self.sch

    def get_schedule_csv(self):
        return self.sch.format_csv()

    def complete_apt(self, apt_number: int):
        self.sch.complete_apt(apt_number)

    def book_apt(self, apt: Appointment):
        self.sch.book_apt(apt)

    def format_csv(self):
        return f"{self.organization_number},{self.name},{self.age},{self.present}"

    def format_bytes(self):
        return str.encode(self.format_csv())

    def get_info(self):
        return [self.organization_number, self.name, self.age, self.present]

    def format_csv_w_sch(self):
        return f"{self.format_csv()},{self.get_schedule_csv()}"
