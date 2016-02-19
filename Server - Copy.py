##*********************************************************************
## File: Server.py
## Name: Taylor H. Paul
## Course: CS3502 Computer Networks
## Project: Game Project
## Operating Environment: Windows 10 Pro
## Compiler: PyCharm 5.0.4, Python 3.4.3
## Date: 29 Jan 16
## Description: This file contains the source code for a server that will
## run "Guess that Number!" as a networking game.
##*********************************************************************

## Starting Server TCP/IP Connection:
##TCP/IP Code imported from echo_s.py provided by Professor Geoffrey Xie

import socket
import sys
import numpy as np
import threading
import queue

#Establish Global Variables
pSock = []
pGuess = []
pId = 0
lock = threading.Lock()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def establishServer():

    ##Establish parameters for TCP/IP Connection
    if len(sys.argv) < 3:
        print ("Need to provide <hostname> <port>, e.g., localhost in the command line!")
        exit(1)

    # Bind the socket to the address given on the command line
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    server_address = (server_name, server_port)
    print("starting up on %s port %s" % server_address)
    sock.bind(server_address)


def pThread(pId):
    waiting = True
    while (waiting):
        sock.listen(1)
        print("waiting for a connection")

        connection, socket  = sock.accept()
        pSock.append((connection, socket))
        try:
            print("client connected:",pSock[pId][1])
            #while (guessCount < 5):
            pGuess.append(connection.recv(16)) #16 characters at a time
            print("received %s" % pGuess[pId])
            # if pGuess[pId]:
            #     connection.sendall(message.encode())
            #     if message == "1": #Answer was right so pick new randowm number:
            #         answer=np.random.randint(1,100,1)
            #waiting = False
        finally:
            connection.close()

    return 0

def quitServer():

    print("The server is now shutting down!!!")



def checkAnswer(answer, guess):

    if answer == int(guess.decode()):
        message = 1         #Client interprets as right answer!
    else:
        message = 2         #Client Interprets as wrong answer!

    return message

##Main Program:



#Establish the Server:
establishServer()

#Generate First Random Number:
answer = np.random.randint(1,100,1) #Using Numpy Random Pick an integer b/t 1-100:

#Wait for clients to make connections:
gameOn = True
while (gameOn):
    if pId < 25:
        t=threading.Thread(target=pThread, args=(pId))
        t.start()
        pId += 1
    else:
        gameOn = False







#