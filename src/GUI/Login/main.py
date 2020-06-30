# This Python file uses the following encoding: utf-8
import sys
import os

from socket import socket

from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.load_ui()
        self.setWindowTitle("Login Window")

        self.conn = socket() # empty socket connection

        # Collect all of our UI elements
        self.loginButton = self.findChild(QtWidgets.QPushButton, "login_Button")
        self.cancelButton = self.findChild(QtWidgets.QPushButton, "cancel_Button")
        self.usernameLineEdit = self.findChild(QtWidgets.QLineEdit, "username_LineEdit")
        self.passwordLineEdit = self.findChild(QtWidgets.QLineEdit, "password_LineEdit")

        #Functionality
        self.loginButton.clicked.connect(self.login) # Associate the clicked event to the login function
        self.cancelButton.clicked.connect(self.cancel) # Associate the clicked event to the cancel function

    def connectSocket(self, conn):
        self.conn = conn

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        #Add functionality here to log onto the server
        data = str.encode(f"/login,{username},{password}")
        self.conn.sendall(data)
        data = self.conn.recv(1024).decode().split(",")

        if(data[0] == "/yes"):
            print("successful login")
            self.close()
        else:
            print("unsuccessful login")
            self.cancel()

    def cancel(self):
        self.usernameLineEdit.clear()
        self.passwordLineEdit.clear()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    HOST = 'ec2-3-21-205-199.us-east-2.compute.amazonaws.com'
    PORT = 12345

    sock = socket()
    sock.connect((HOST, PORT))

    app = QApplication([])
    widget = LoginWindow()

    widget.connectSocket(sock)

    widget.show()
    sys.exit(app.exec_())
