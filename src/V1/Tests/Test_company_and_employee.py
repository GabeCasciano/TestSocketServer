# Testing the company and employee classes

import sys
import time
sys.path.append("..")

from src.Utils.Employee import Employee

# To Create an employee
# test functionality

Name = "Gabe"
Department = "Engineering"

Name2 = "Brandon"
Department2 = "Learning"

Gabe = Employee(Name, Department)  # Create an employee
Brandon = Employee(Name2, Department2) # Create a second employee

# printing the current location and last time seen of employee
print("{}, {}".format(Gabe.employee_on_site()[0], Gabe.employee_on_site()[1]))
print("{}, {}".format(Brandon.employee_on_site()[0], Brandon.employee_on_site()[1]))

time.sleep(1) # sleeping

# Checking employees in
Gabe.check_in()
Brandon.check_in()

# Print location information again
print("{}, {}".format(Gabe.employee_on_site()[0], Gabe.employee_on_site()[1]))
print("{}, {}".format(Brandon.employee_on_site()[0], Brandon.employee_on_site()[1]))

time.sleep(1)

# Check one out
Gabe.check_out()

# Print location information again again
print("{}, {}".format(Gabe.employee_on_site()[0], Gabe.employee_on_site()[1]))
print("{}, {}".format(Brandon.employee_on_site()[0], Brandon.employee_on_site()[1]))

time.sleep(1)

# Check the other out
Brandon.check_out()

# Print location information again again
print("{}, {}".format(Gabe.employee_on_site()[0], Gabe.employee_on_site()[1]))
print("{}, {}".format(Brandon.employee_on_site()[0], Brandon.employee_on_site()[1]))

from src.Utils.Company import Company

DankCompany = Company("Brandons & Gabes Dank Memes Llc.")

DankCompany.add_employee(Name, Department)
DankCompany.add_employee(Name2, Department2)


for emp in DankCompany.employees:
    print(emp.toString())
    emp.check_in()

time.sleep(1)

for emp in DankCompany.employees:
    print(emp.toString())
    emp.check_out()

DankCompany.check_in_by_name(Name)

for emp in DankCompany.employees:
    print(emp.toString())

print("Adding Jetson")

Name3 = "Jetson"
Department3 = "Computers"

jet = Employee(Name3, Department3)

DankCompany.add_existing_employee(jet)

print("Employees:")
print(DankCompany.toString())

print("Employees:")
DankCompany.add_existing_employee(Gabe)

print(DankCompany.toString())

Hamza = Employee("Hamza", "Br00")

DankCompany.add_existing_employee(Hamza)

print("Employees:")
print(DankCompany.toString())

DankCompany.remove_employee_by_name(Name)

print("Employees:")
print(DankCompany.toString())

DankCompany.remove_employee_by_ID(4)

print("Employees:")
print(DankCompany.toString())