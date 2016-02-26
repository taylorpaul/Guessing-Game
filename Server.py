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

ERRORVALUE=500

#Establish Global Variables
pSock = [] # List of Players: [(connection1, socket1),(connection2, socket2)...]
pGuess = {} # Dictionary of ByteCode Guesses: {pId1: Guess1}
pId = 0
lock = threading.Lock()
gameOn= True

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(25)


#----------------------------------------------------------------------
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

#----------------------------------------------------------------------------------
def pThread(pId, lock):

    global pGuess
    print("client connected:",pSock[pId][1])

    try:
        response = pSock[pId][0].recv(16) #16 characters at a time

    except: #If a timout occurs before receiving guess, client handles errors
        response = str(ERRORVALUE).encode() #Store ERRORVALUE, therefore they cannot win

    lock.acquire()
    pGuess[str(pId)] = response
    lock.release()
    print("received %s" % pGuess[str(pId)])

    return 0

#----------------------------------------------------------------------------------
def closeConnections():

    for p in range(0,len(pSock)):
        pSock[p][0].close()
    print("The server is now starting a new game!!!")
    startGame()

    return 0

#----------------------------------------------------------------------------------
def checkAnswer(answer):

    global gameOn
    gameOn = False #End game (prevent further connections) once called
    global pGuess
    winner=[]
    lock.acquire()

    #Create list of absolute differences between answer and guesses

    for p in range(0,(len(pGuess))):
        winner.append(int(abs(answer-int(pGuess[str(p)].decode()))))

    #Find the minimum guess difference to the answer:
    win_ans = min(winner)

    #Locate all indices for all winners (if len>1 there are ties)
    win_ids = [i for i, x in enumerate(winner) if x == win_ans]

    lock.release()
    sendWinner(win_ids, answer)
    closeConnections()
    print("About to exit CheckAnswer()")
    exit()
    return


#----------------------------------------------------------------------------------
def sendWinner(win_ids, answer):

    #Get a count of winners:
    win_count=len(win_ids)

    #Create a string of winning answers:
    win_ans =str(win_count) #add count of winners to front

    #add each winning quess to end of answer list (will be 1 if no ties):
    for winner in win_ids:
        win_ans = win_ans + ', ' + str(pGuess[str(winner)].decode())

    #Combine into 1 string and send:
    for p in range(0,len(pSock)):
        if p in win_ids:
            win_mess = '1, ' +str(answer)+', '+ win_ans# 1 for winner, the answer, winning answers

        else:
            win_mess = '2, ' +str(answer)+', '+ win_ans #2 for loser, the answer, winning answers

        pSock[p][0].sendall(win_mess.encode())

    return 0

#----------------------------------------------------------------------------------
def startGame():

    global pId
    pId = 0
    global gameOn
    gameOn = True
    global pSock
    pSock = []
    global pGuess
    pGuess = {}
    answer = np.random.randint(1,100,1) #Using Numpy Random Pick an integer b/t 1-100:


    while (gameOn):

        sock.listen(1)
        print("Waiting for a connection...")

        if pId < 25:

            try:
                connection, socket = sock.accept()
            except OSError: #If timeout occurs

                if pId < 2: #Check to see if less than two players joined
                    if pId == 1: #If only 1 player send waiting message
                        waiting = "noFriends"
                        pSock[0][0].sendall(waiting.encode())
                    continue

                else: #Exit the while Loop
                    break

            pSock.append((connection, socket))
            t=threading.Thread(target=pThread, args=(pId, lock))
            t.daemon = True #Allow main process to exit before threads are finished
            t.start()

            if pId == 1:
                time = threading.Timer(30.0, checkAnswer, args=answer)
                time.start()

            pId += 1

        else:
            gameOn = False

    time.join() # Wait for checkanswer() to complete before starting a new game
    return


##Main Program:----------------------------------------------------------------------------------

#Establish the Server:
establishServer()

#Keep the game going until someone closes the server:
while True:
    print("Creating First Thread")
    game = threading.Thread(startGame())
    print("About to Start first game!")
    game.start()
    print("First Game Started")
    game.join()
    print("Next Game Started")

#   Start Server:  python server.py localhost 1000
