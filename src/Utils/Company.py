from .Employee import Employee
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "backup.db")

class Company():

    def __init__(self, Name):
        self.employees = []
        self.Name = Name
        self.Backup_location = db_path
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

    def toSQL(self):
        parameters = []
        for emp in self.employees:
            parameters.append(emp.toSQL())

        return parameters

    def create_db(self):
        conn = sqlite3.connect(self.Backup_location)
        c = conn.cursor()
        create_table = '''CREATE TABLE EMPLOYEES (
                                ID INT PRIMARY KEY NOT NULL,
                                NAME TEXT NOT NULL,
                                DEPARTMENT TEXT NOT NULL,
                                LAST_SEEN INT NOT NULL,
                                ON_SITE NUMERIC NOT NULL)'''

        c.execute(create_table)
        conn.commit()
        conn.close()

    def save_to_file(self):
        conn = sqlite3.connect(self.Backup_location)
        c = conn.cursor()

        insert_emp = 'INSERT INTO EMPLOYEES VALUES (?,?,?,?,?)'

        c.executemany(insert_emp, self.toSQL())
        conn.commit()
        conn.close()

    def read_from_file(self):
        conn = sqlite3.connect(self.Backup_location)
        c = conn.cursor()

        select_emp = 'SELECT * FROM EMPLOYEES'

        c.execute(select_emp)
        list = c.fetchall();

        for l in list:
            emp = Employee(str(l[1]), str(l[2]))
            emp._set_id(int(l[0]))
            self.add_existing_employee(emp)

        conn.close()
