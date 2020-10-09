from .Organization.Company import Company
from .Organization.Employee import Employee
from .Organization.Client import Client
from .Organization.Person import Person

from socket import socket
from threading import Thread

HOST = ""
PORT = 12345

Corp = Company("Brandon Corp")

class Server(Thread):

    class Client(Thread):
        def __init__(self, conn: socket):
            Thread.__init__(self)
            self.conn = conn
            self.running = True

        def run(self) -> None:
            while self.running:
                try:
                    data_packet = self.conn.recv(2048).split(",")
                    command = data_packet[0]
                    specifier = data_packet[1]
                    data = data_packet[2].split(";")

                    if command == 1:
                        emp, cust = Corp.get_info()
                        out = ""
                        for e in emp:
                            out += e
                        for c in cust:
                            out += c
                        self.conn.sendall(str.encode(out))

                    elif command == 2:
                        pass

                    elif command == 3:
                        if specifier == 1:
                            temp = Corp.get_person_info(name=data[0])
                        elif specifier == 2:
                            temp = Corp.get_person_info(number=data[0])
                        if temp != None:
                            self.conn.sendall(temp.format_bytes())

                    elif command == 4:
                        if specifier == 1:
                            temp = Corp.get_person_info(name=data[0]).present
                        elif specifier == 2:
                            temp = Corp.get_person_info(number=data[0]).present
                        if temp != None:
                            self.conn.sendall(str.encode(f"{temp}"))

                    elif command == 66:
                        self.running = False

                except socket.error as e:
                    print(e)
            self.conn.detach()
            self.conn = None

    class User(Thread):
        def __init__(self, conn: socket):
            Thread.__init__(self)
            self.conn = conn
            self.running = True

    class Jetson(Thread):
        def __init__(self, conn: socket):
            Thread.__init__(self)
            self.conn = conn
            self.running = True

        def run(self) -> None:
            self.conn.settimeout(1)
            while self.running:
                try:
                    data_packet = self.conn.recv(256).decode().split(",")
                    command = data_packet[0]
                    specifier = data_packet[1]
                    data = int(data_packet[2])

                    if command == 1:
                        if specifier == 1:
                            p = Corp.get_person_info(number=data)
                            Corp.toggle_location(p)
                            self.conn.sendall(str.encode("posak"))
                    if command == 66:
                        self.running = False

                except socket.error as e:
                    print(e)
            self.conn.detach()
            self.conn = None

    def __init__(self):
        Thread.__init__(self)
        self.thread_pool = []
        self.running = True
        self.conn = socket()
        self.conn.bind((HOST, PORT))
        self.conn.listen()

    def run(self) -> None:
        while self.running:
            new_conn = self.conn.accept()[0]
            data = new_conn.recv(256).decode()
            t = None
            if data == "Jetson":
                t = self.Jetson(new_conn)
                new_conn.sendall(str.encode("posak"))
                t.start()
                self.thread_pool.append(t)

            elif data == "Client":
                t = self.Client(new_conn)
                new_conn.sendall(str.encode("posak"))
                t.start()
                self.thread_pool.append(t)

            else:
                new_conn.sendall(str.encode("negak"))

        for t in self.thread_pool:
            t.join()

if __name__ == "__main__":
    server = Server()
    server.start()