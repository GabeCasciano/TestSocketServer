# This Python file uses the following encoding: utf-8
import sys
import os
from threading import Thread
from socket import socket
import time


from PySide2 import QtWidgets, QtGui
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader


class UserWindow(QWidget):
    def __init__(self):
        super(UserWindow, self).__init__()
        self.load_ui()

        # Collect all of the UI Elements
        # -- Buttons
        self.createEmpButton = self.findChild(QtWidgets.QPushButton, "newEmp_create_Button")
        self.removeEmpButton = self.findChild(QtWidgets.QPushButton, "remEmp_remove_Button")
        self.clearEmpButton = self.findChild(QtWidgets.QPushButton, "empClear_Button")
        self.clearCompanyButton = self.findChild(QtWidgets.QPushButton, "clearCompany_Button")

        self.clearCompanyButton.setStyleSheet("background-color:rgb(255,0,0)")
        # -- Line Edits
        self.newEmpNameLineEdit = self.findChild(QtWidgets.QLineEdit, "newEmp_name_LineEdit")
        self.newEmpDeptLineEdit = self.findChild(QtWidgets.QLineEdit, "newEmp_department_LineEdit")
        self.remEmpNameLineEdit = self.findChild(QtWidgets.QLineEdit, "remEmp_name_LineEdit")
        self.remEmpIDLineEdit = self.findChild(QtWidgets.QLineEdit, "remEmp_ID_LineEdit")

        # -- Table Widget
        self.employeeTable = self.findChild(QtWidgets.QTableWidget, "EmployeesTableWidget")
        # -- Tab Widget
        self.tabs = self.findChild(QtWidgets.QTabWidget, "empFunc_TabWidget")
        # Give Functionality to everything
        self.createEmpButton.clicked.connect(self.createEmp)
        self.removeEmpButton.clicked.connect(self.removeEmp)
        self.clearEmpButton.clicked.connect(self.clear_tabs)
        self.tabs.currentChanged.connect(self.clear_tabs)

        self.flag = True
        self.conn = socket()
        #self.t_update = Thread(target=self.updateTable(), args=self) # create a thread running updateTable function

    def connectConn(self, conn):
        self.conn = conn
        self.updateTable()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def clear_tabs(self):
        self.newEmpNameLineEdit.clear()
        self.newEmpDeptLineEdit.clear()
        self.remEmpIDLineEdit.clear()
        self.remEmpNameLineEdit.clear()

    def createEmp(self): # Test me
        name = self.newEmpNameLineEdit.text()
        dept = self.newEmpDeptLineEdit.text()

        if self.conn is not None:
            data = str.encode(f"/new_emp,{name},{dept}")
            self.conn.sendall(data)
            data = self.conn.recv(1024).decode().split(",")

            if len(data) >= 1:
                self.updateTable()
        self.clear_tabs()
        self.updateTable()

    def removeEmp(self): # Test me 2
        name = self.remEmpNameLineEdit.text()
        ID = self.remEmpIDLineEdit.text()

        if self.conn is not None:
            if ID == "":
                data = str.encode(f"/remove_emp,{1},{name}")
            else:
                data = str.encode(f"/remove_emp,{2},{ID}")
            self.conn.sendall(data)
            data = self.conn.recv(1024).decode().split(",")

            if data[0] == "True":
                self.updateTable()

        self.clear_tabs()

    def updateTable(self): # use a thread to trigger this event periodically
        employees = []

        data = str.encode("/get_company")
        self.conn.sendall(data)

        data = self.conn.recv(1024).decode().split(",") # recv size of company

        if data[0] == "/size":
            inputsize = int(data[1]) + 128

            data = self.conn.recv(inputsize).decode()
            if "STOP" in data:
                return

            data = data.split(";")
            for r in data:
                if r != '':
                    employees.append(r.split(","))


        ROW = len(employees); COL = 5
        self.employeeTable.setRowCount(ROW)
        for r in range(0,ROW):
            for c in range(0, COL):
                self.employeeTable.setItem(r,c, QtWidgets.QTableWidgetItem(str(employees[r][c])))


if __name__ == "__main__":
    HOST = 'ec2-3-21-205-199.us-east-2.compute.amazonaws.com'
    PORT = 12345

    sock = socket()
    sock.connect((HOST, PORT))

    app = QApplication([])
    widget = UserWindow()
    widget.connectConn(sock)
    widget.show()
    sys.exit(app.exec_())
