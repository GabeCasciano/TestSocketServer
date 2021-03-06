import socket
import datetime

HOST = ''
PORT = 12345

print("Starting program {}".format(datetime.datetime.now()))

sock = socket.socket() # Socket to bind to the host
conn = socket.socket() # Socket to connect to the client
IP = socket.gethostbyname(socket.gethostname()) # local ip address of the server

print("Host device local IP {}".format(IP))

sock.bind((HOST, PORT)) # bind socket to server
IP_2 = sock.getsockname()[0] # Public IP of Host server

print("Successfully bound to addr {} on port {}".format(HOST, PORT))

sock.listen() # listen for users connection

run = True

try:
    print("Listening for new client ...")
    conn, addr = sock.accept()  # accept a new connection on the server

    while run:
        data = conn.recv(2048) # receive 2048 bytes of data from client
        text = data.decode() # decode data sent from client

        print("Received Data from client {}, msg: {}".format(addr, text)) # format and display

        data = "Server says Hello, {}, time {}".format(text, datetime.datetime.now())

        if text == "/close" or text == "/exit":
            run = False
            data = "server is closing connection, bye"
        elif text == "/time":
            data = "server time is {}".format(datetime.datetime.now())
        conn.sendall(str.encode(data))

except KeyboardInterrupt: # if interrupted by sys admin
    print("Closing server")
finally:
    conn.close()

sock.close() # close socket
exit(0)
