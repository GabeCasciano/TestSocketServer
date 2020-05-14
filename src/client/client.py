import socket

HOST = '' # Host server IPv4 addr or public dns
PORT = 12345 # Port that the server is listening on

sock = socket.socket() # Create socket object
IP = socket.gethostbyname(socket.gethostname()) # get local host IP addr
sock.connect((HOST, PORT)) # connect the socket to the server
IP_2 = sock.getsockname()[0] # Public IP of Host server

text = "This is gabe to server" # the text that we want to send to the server
data_packet = str.encode(text) # the converted data packet that will be sent
sock.sendall(data_packet) # sending the data to the server

sock.close() # close socket connection

