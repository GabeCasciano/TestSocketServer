import sys
sys.path.append("..")

from src.Utils.Employee import Employee # Custom Employee class
from src.Utils.Company import Company # Custom Company class

from socket import socket # Socket object
from datetime import datetime # Datetime object

# Company variables and set up

company = Company("This company")

# Networking variables and set up

MAX_CLIENTS = 2 # Var for max clients on server
MAX_DATA_LEN = 256 # Max Data received

HOST = '' # Host addr
PORT = 12345 # Host port

with_client = True
run = True

host_sock = socket() # Host socket object
client_sock = socket() # Client socket object
client_addr = 0 # Client addr

host_sock.bind((HOST, PORT)) # Bind host to PORT
host_sock.listen(MAX_CLIENTS) # listen for MAX_CLIENTS amount of clients

try:
    while run:
        with_client = True
        print("Waiting for client ...")
        client_sock, client_addr = host_sock.accept() #

        while with_client:
            data = client_sock.recv(MAX_DATA_LEN)
            data = data.decode()
            print("\nCurrent Company: ")
            print(company.toString())

            print(f"Data received from addr, {client_addr}, {data}")

            out = data.split(",")

            data_len = len(out)

            command = out[0]  # Extract our command from received string

            if command == "/close":
                with_client = False
                data = f"Connection Closed, {datetime.now()}"
                data = str.encode(data)
                client_sock.sendall(data)
                client_sock.close()


                print(f"Sending to client conn {client_addr}, {data.decode()}")
                print(f"Closing client conn {client_addr}, {datetime.now()}")
                break

            elif command == "/shutdown" or command == "/reboot":
                with_client = False
                run = False
                data = f"Connection Closed and server shutting down, {datetime.now()}"
                data = str.encode(data)
                client_sock.sendall(data)
                client_sock.close()

                print(f"Sending to client conn {client_addr}, {data.decode()}")
                print(f"Closing client conn {client_addr}, {datetime.now()}")
                print(f"Closing server {datetime.now()}")

                break

            elif command == "/time":
                data = f"{datetime.now()}"
                data = str.encode(data)
                client_sock.sendall(data)

                print(f"Sending to client conn {client_addr}, {data.decode()}")
                print(f"Client conn {client_addr} requesting server time, {datetime.now()}")

            elif command == "/new_emp":
                # Command String:  /new_emp,<Name>,<Department>
                data = ""
                emp = None

                if data_len >= 3:
                    emp = company.add_employee(out[1], out[2])

                if emp != None:
                    data = emp.toBytes()
                    print(f"New Employee: {data}, {datetime.now()}")

                else:
                    data = str.encode(f"{False}")

                client_sock.sendall(data)

                print(f"Sending to client conn {client_addr}, {data.decode()}")

            elif command == "/remove_emp":
                # Command String: /remove_emp,<Specifier>,<Data>
                # <Specifier> = 1 - Name, 2 - ID
                data = ""
                complete = False

                if data_len >= 3:

                    if int(out[1]) == 1: # Name
                        complete = company.remove_employee_by_name(out[2])

                    elif int(out[1]) == 2: # ID
                        complete = company.remove_employee_by_ID(int(out[2]))

                    print(f"Removed Employee: {out[2]}, {complete}, {datetime.now()}")

                data = str.encode(f"{complete}")
                client_sock.sendall(data)

                print(f"Sending to client conn {client_addr}, {data.decode()}")

            elif command == "/check_in":
                # Command String: /check_in,<Specifier>,<Data>
                # <Specifier> = 1 - Name, 2 - ID
                data = ""
                complete = False

                if data_len >= 3:
                    if int(out[1]) == 1:  # Name
                        complete = company.check_in_by_name(out[2])

                    elif int(out[1]) == 2:  # ID
                        complete = company.check_in_by_ID(int(out[2]))

                    print(f"Check-In Employee: {out[2]}, {complete}, {datetime.now()}")

                data = str.encode(f"{complete},{datetime.now()}")
                client_sock.sendall(data)

                print(f"Sending to client conn {client_addr}, {data.decode()}")

            elif command == "/check_out":
                # Command String: /check_out,<Specifier>,<Data>
                # <Specifier> = 1 - Name, 2 - ID
                data = ""
                complete = False

                if data_len >= 3:
                    if int(out[1]) == 1:  # Name
                        complete = company.check_out_by_name(out[2])

                    elif int(out[1]) == 2:  # ID
                        complete = company.check_out_by_ID(int(out[2]))

                data = str.encode(f"{complete},{datetime.now()}")
                client_sock.sendall(data)

            elif command == "/last_seen":
                # Command String: /last_seen,<Specifier>,<Data>
                # <Specifier> = 1 - Name, 2 - ID
                data = []

                if data_len >= 3:
                    if int(out[1]) == 1:  # Name
                        data = company.last_seen_by_name(out[2])

                    elif int(out[1]) == 2:  # ID
                        data = company.last_seen_by_ID(int(out[2]))

                data = str.encode(f"{data[0]},{data[1]}")
                client_sock.sendall(data)

            elif command == "/backup":
                pass
            elif command == "/load_backup":
                pass
            else:
                print(f"Client conn {client_addr} sent: {data}")
                client_sock.sendall(str.encode(data))

except KeyboardInterrupt:
    print("Killing server")

host_sock.close()
exit(0)