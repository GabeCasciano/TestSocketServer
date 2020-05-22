import datetime


class Employee():

    MASTER_ID = 1

    def __init__(self, Name, Department):
        self.Name = Name
        self.ID = Employee.MASTER_ID
        self.Department = Department
        self.last_seen = datetime.datetime.now() # last time employee was seen on camera
        self.present = False # if the employee is currently at work

        print("New Employee: {}, {}, department: {}".format(self.Name, self.ID, self.Department))

        Employee.MASTER_ID += 1

    def check_in(self):
        self.last_seen = datetime.datetime.now()
        self.present = True

    def check_out(self):
        self.last_seen = datetime.datetime.now()
        self.present = False

    def employee_on_site(self):
        return (self.last_seen, self.present)

    def toString(self):
        return f"Name: {self.Name} Id: {self.ID} Department: {self.Department} Last Time seen: {self.last_seen} On Site: {self.present} "

    def toBytes(self):
        return str.encode(f"{self.Name},{self.ID},{self.Department}")