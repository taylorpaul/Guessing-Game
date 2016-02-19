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

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 10000)
print("connecting to %s port %s" % server_address)
sock.connect(server_address)

try:
    
    message = b"This is the message.  It will be repeated multiple times."
    print("sending %s" % message)
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print("received %s" % data)

finally:
    sock.close()
