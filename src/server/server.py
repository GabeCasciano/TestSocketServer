import socket

HOST = ''
PORT = 12345

sock = socket.socket() # Socket to bind to the host
conn = socket.socket() # Socket to connect to the client
IP = socket.gethostbyname(socket.gethostname()) # local ip address of the server

sock.bind((HOST, PORT)) # bind socket to server
IP_2 = sock.getsockname()[0] # Public IP of Host server
sock.listen() # listen for users connection

run = True

try:
    while run:
        conn, addr = sock.accept() # accept a new connection on the server
        data = conn.recv(2048) # receive 2048 bytes of data from client
        text = data.decode() # decode data sent from client
        print("Recieved Data from client {}, msg: {}".format(text, addr)) # format and display
except KeyboardInterrupt: # if interrupted by sys admin
    conn.close() # close connection to client
    print("Closing server")

sock.close() # close socket
exit(0)