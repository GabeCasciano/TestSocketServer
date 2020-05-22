from socket import socket

HOST = 'ec2-3-21-205-199.us-east-2.compute.amazonaws.com'
PORT = 12345 # 12346 for brandon

sock = socket()
sock.connect((HOST, PORT))

# Send the server data packet, to create new employee
data_packet = str.encode(f"/new_emp,Gabe Casciano,Engineering")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

# Send data packet to terminate connection
data_packet = str.encode(f"/close")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())