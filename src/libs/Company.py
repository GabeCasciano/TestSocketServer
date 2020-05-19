from . import Employee

class Company:

    def __init__(self, Name):
        self.employees = []
        self.Name = Name

    def add_employee(self, Name, Department):
        emp = Employee(Name, Department)
        self.employees.append(emp)
        return emp

    def remove_employee_by_name(self, Name):
        for emp in self.employees:
            if emp.Name == Name:
                self.employees.remove(emp)

    def remove_employee_by_ID(self, ID):
        for emp in self.employees:
            if emp.ID == ID:
                self.employees.remove(emp)
