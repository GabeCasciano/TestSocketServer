from .Employee import Employee

class Company():

    def __init__(self, Name):
        self.employees = []
        self.Name = Name
        print("New Company: {}".format(Name))

    def add_existing_employee(self, employee):
        flag = False # Flag for customer already existing

        #Check the entire list of companies
        for emp in self.employees:
            if emp.Name == employee.Name or emp.ID == employee.ID:
                print("already exists in company")
                flag = True # set flag if employee alrady exists
                break

        if not flag:
            self.employees.append(employee) # Create employee if flag is not set

        return not flag

    def add_employee(self, Name, Department):
        emp = Employee(Name, Department)
        self.employees.append(emp)
        return emp

    def check_in_by_name(self, Name):
        for emp in self.employees:
            if emp.Name == Name:
                emp.check_in()
                return True
        return False

    def check_in_by_ID(self, ID):
        for emp in self.employees:
            if emp.ID == ID:
                emp.check_in()
                return True
        return False

    def check_out_by_name(self, Name):
        for emp in self.employees:
            if emp.Name == Name:
                emp.check_out()
                return True
        return False

    def check_out_by_ID(self, ID):
        for emp in self.employees:
            if emp.ID == ID:
                emp.check_out()
                return True
        return False

    def remove_employee_by_name(self, Name):
        for emp in self.employees:
            if emp.Name == Name:
                self.employees.remove(emp)
                return True
        return False

    def remove_employee_by_ID(self, ID):
        for emp in self.employees:
            if emp.ID == ID:
                self.employees.remove(emp)
                return True
        return False

    def last_seen_by_ID(self, ID):
        for emp in self.employees:
            if emp.ID == ID:
                return emp.employee_on_site()
        return (-1,-1)

    def last_seen_by_name(self, Name):
        for emp in self.employees:
            if emp.Name == Name:
                return emp.employee_on_site()
        return (-1,-1)

    def toString(self):
        String = ""
        for emp in self.employees:
            String += emp.toString() + "\n"

        return String

    def save_to_file(self):
        pass

    def read_from_file(self):
        pass
