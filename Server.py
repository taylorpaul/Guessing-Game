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
pSock = [] # List of Players: [(connection1, socket1),(connection2, socket2)...]
pGuess = [] # List of ByteCode Guesses: [GuessP1,GuessP2...]
pId = 0
lock = threading.Lock()
gameOn = True

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(30)



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


def pThread(pId, lock):

    try:
        if gameOn: #Check to see if client connected after game closed
            print("client connected:",pSock[pId][1])
            #while (guessCount < 5):
            lock.acquire()
            pGuess.append(pSock[pId][0].recv(16)) #16 characters at a time
            lock.release()
            print("received %s" % pGuess[pId])
        # if pGuess[pId]:
        #     connection.sendall(message.encode())
        #     if message == "1": #Answer was right so pick new randowm number:
        #         answer=np.random.randint(1,100,1)
        #waiting = False
    finally:
        return 0

def closeConnections():
    for p in range(0,len(pSock)):
        pSock[p][0].close()
    print("The server is now starting a new game!!!")
    return 0


def checkAnswer(answer):

    global gameOn
    gameOn = False #End game (prevent further connections) once called
    winner=[]
    lock.acquire()

    #Create list of absolute differences between answer and guesses
    for p in range(0,len(pGuess)):
        winner.append(int(abs(answer-int(pGuess[p].decode()))))

    #Find winner that is closest!
    win_ans = min(winner)
    win_id = winner.index(win_ans)
    lock.release()
    sendWinner(win_id, answer)
    return 0

def sendWinner(win_id, answer):

    #
    for p in range(0,len(pSock)):
        if p ==win_id:
            win_mess = '1,' + str(answer) +', ' + str(pGuess[win_id].decode())# 1 for winner, along with the answer, winner guess
        else:
            win_mess = '2, ' + str(answer) +', ' + str(pGuess[win_id].decode()) #2 for loser, along with answer, winner guess

        pSock[p][0].sendall(win_mess.encode())

    return 0

def startGame():
    global pId
    pId = 0
    global gameOn
    gameOn = True
    global pSock
    pSock = []
    global pGuess
    pGuess = []
    answer = np.random.randint(1,100,1) #Using Numpy Random Pick an integer b/t 1-100:

    while (gameOn):

        sock.listen(1)
        print("waiting for a connection")

        if pId < 25:
            try:
                connection, socket = sock.accept()
            except OSError: #If timeout occurs exit while loop
                break
            pSock.append((connection, socket))
            t=threading.Thread(target=pThread, args=(pId, lock))
            t.start()
            if pId == 1:
                time = threading.Timer(10.0, checkAnswer, args=answer)
                time.start()
            pId += 1

        else:
            gameOn = False

    return

##Main Program:

#Establish the Server:
establishServer()

#start the first game:
while True:

    startGame()
    closeConnections()

#TODO Interpret winning/losing results at the client!