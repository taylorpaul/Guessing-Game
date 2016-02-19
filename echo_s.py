# 
# Revised to work with Python version 3.4
#
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) < 2:
    print ("Need to provide <hostname>, e.g., localhost in the command line!")
    exit(1)
    
# Bind the socket to the address given on the command line
server_name = sys.argv[1]
server_address = (server_name, 10000)
print("starting up on %s port %s" % server_address)
sock.bind(server_address)
sock.listen(1)

while True:
    print("waiting for a connection")
    connection, client_address = sock.accept()
    try:
        print("client connected:", client_address)
        while True:
            data = connection.recv(16) #16 characters at a time
            print("received %s" % data)
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()
