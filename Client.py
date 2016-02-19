##*********************************************************************
## File: Client.py
## Name: Taylor H. Paul
## Course: CS3502 Computer Networks
## Project: Game Project
## Operating Environment: Windows 10 Pro
## Compiler: PyCharm 5.0.4, Python 3.4.3
## Date: 29 Jan 16
## Description: This file contains the source code for a cleint that will
## run "Guess that Number!" as a networking game.
##*********************************************************************


## Starting Server TCP/IP Connection:
##Following code imported from echo_s.py provided by Professor Geoffrey Xie
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a TCP/IP socket

def connect2server():

    if len(sys.argv) < 3:
        print ("Need to provide <hostname> <port>, e.g., localhost in the command line!")
        exit(1)

    # Connect the socket to the port on the server given by the caller
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    server_address = (server_name, server_port)
    print("connecting to %s port %s" % server_address)
    sock.connect(server_address)

    return 0

def guessSend():
    guess=getvalidinput()

    print("sending %s" % guess)
    try:
        sock.sendall(guess.encode())

        amount_received = 0
        amount_expected = len(guess.encode())

        count = 0

        while (amount_received < amount_expected) and (count <= 25):
            data = sock.recv(16)
            if data:  ##Only print if receiving data
                amount_received += len(data)
                print("received %s" % data.decode())
            count+=1 ##Allow 25 loops without data before exiting loop
        print(data.decode)
    except ConnectionResetError or ConnectionAbortedError:
        print("Your guess was not received before the game ended, sorry :-(...reconnect and try again")
        return
    return data.decode()

def quitGuess():

    print("Thanks for playing!!! Closing Connection!")
    sock.close()
    return

##----------------------------------------------------------------------------------
def getvalidinput():
    """Requests a user input for the guess, converts to an integer for checking value is between 1-100, if
    not it prompts the user again, if it is in returns the valid response as a string for further use by
    the program."""
    try:
        response = int(input("What number would you like to guess? (### from 1-100): "))
    except: #If a user inputs a special character or letter
        print("\nInvalid guess, please guess an integer from 1-100 in format ###\n")
        response = int(input("What number would you like to guess? (### from 1-100): "))

    while (1 > response) or (response > 100):

        print("\nInvalid guess, please guess an integer from 1-100 in format ###\n")
        response = int(input("What number would you like to guess? (### from 1-100): "))

    return str(response)




## MAIN PROGRAM:

connect2server()
win_mess=guessSend()
#checkWinner(win_mess)
quitGuess()

