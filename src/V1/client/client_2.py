import socket
import datetime
import random

HOST = 'ec2-3-21-205-199.us-east-2.compute.amazonaws.com' # Host server IPv4 addr or public dns
PORT = 12345 # Port that the server is listening on

sock = socket.socket()

print("Starting client shell")

print("Connecting to; {}, on port; {}, at: {}".format(HOST, PORT, datetime.datetime.now()))
sock.connect((HOST, PORT))
print("Successfully connected")

run = True

try:
    while run:
        print("Enter a command or message")
        text = input()

        DATA_LEN = 2048

        data_packet = str.encode(text)
        sock.sendall(data_packet)

        if text == "/close":
            run = False
        elif text == '/get_company':
            DATA_LEN = 4096

        data_packet = sock.recv(DATA_LEN)
        print("Received from server, {}, at: {}".format(data_packet.decode(), datetime.datetime.now()))



except KeyboardInterrupt:
    print("Closing connection")
finally:
    sock.sendall(str.encode("/close"))
    sock.close()

