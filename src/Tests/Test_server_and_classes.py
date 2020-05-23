from socket import socket
import time

HOST = 'ec2-3-21-205-199.us-east-2.compute.amazonaws.com'
PORT = 12345 # 12346 for brandon

sock = socket()
sock.connect((HOST, PORT))

# Send the server data packet, to create new employee
data_packet = str.encode(f"/new_emp,Gabe Casciano,Engineering")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

# Send a data packet, to create a new employee
data_packet = str.encode(f"/new_emp,Brandon Chow,Engineering")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

# Send  data packet, to remove and employee
data_packet = str.encode(f"/remove_emp,1,Brandon Chow")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

# Send  data packet, to remove and employee
data_packet = str.encode(f"/remove_emp,2,1")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

# Send the server data packet, to create new employee
data_packet = str.encode(f"/new_emp,Gabe Casciano,Engineering")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

# Send the server data packet, to check in employee
data_packet = str.encode(f"/check_in,1,Gabe Casciano")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

time.sleep(2)

# Send the server data packet, to check out employee
data_packet = str.encode(f"/check_out,1,Gabe Casciano")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

# Send the server data packet, to check in employee
data_packet = str.encode(f"/check_in,2,3")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())

time.sleep(2)

# Send the server data packet, to check out employee
data_packet = str.encode(f"/check_out,2,3")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())


# Send data packet to terminate connection
data_packet = str.encode(f"/close")
sock.sendall(data_packet)
data = sock.recv(1024)
print(data.decode())