import sys
from PySide2 import QtCore, QtWidgets, QtGui

class Login(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Please")
        self.username_box = QtWidgets.QLineEdit("User-Name")
        self.password_box = QtWidgets.QLineEdit("Password")

        self.enter = QtWidgets.QPushButton("Enter")
        self.cancel = QtWidgets.QPushButton("Cancel")

        self.username_box.resize(100, 50)
        self.password_box.resize(100, 50)
        self.enter.resize(75, 50)
        self.cancel.resize(75, 50)

        self.username_box.setClearButtonEnabled(True)
        self.password_box.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_box.setClearButtonEnabled(True)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.username_box, 0, 0)
        self.layout.addWidget(self.password_box, 1, 0)
        self.layout.addWidget(self.enter, 0, 1)
        self.layout.addWidget(self.cancel, 1, 1)

        self.setLayout(self.layout)

        self.enter.clicked.connect(self.submit_password)
        self.cancel.clicked.connect(self.cancel_)

    def submit_password(self):
        username = self.username_box.text()
        password = self.password_box.text()
        print(f"{username}, {password}")

    def cancel_(self):
        self.username_box.clear()
        self.password_box.clear()


if __name__ == "__main__":
    login = QtWidgets.QApplication([])

    widget = Login()
    widget.show()

    sys.exit(login.exec_())