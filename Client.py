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

print(" _      ________   _________  __  _______                   ")
print("| | /| / / __/ /  / ___/ __ \/  |/  / __/                   ")
print("| |/ |/ / _// /__/ /__/ /_/ / /|_/ / _/                     ")
print("|__/|__/___/____/\___/\____/_/  /_/___/                     ")
print("                                                            ")
print(" __________                                                 ")
print("/_  __/ __ \                                                ")
print(" / / / /_/ /                                                ")
print("/_/  \____/                                                 ")
print("                                                            ")
print("  _______  ___________________  _______                     ")
print(" / ___/ / / / __/ __/ __/  _/ |/ / ___/                     ")
print("/ (_ / /_/ / _/_\ \_\ \_/ //    / (_ /                      ")
print("\___/\____/___/___/___/___/_/|_/\___/                       ")
print("                                                            ")
print("  ________   __  _______                                    ")
print(" / ___/ _ | /  |/  / __/                                    ")
print("/ (_ / __ |/ /|_/ / _/                                      ")
print("\___/_/ |_/_/  /_/___/                                      ")
print("                                                            ")
print("   ___  ___  ___  ___                                       ")
print("  |_  |/ _ \/ _ \/ _ \                                      ")
print(" / __// // / // / // /                                      ")
print("/____/\___/\___/\___/                                       ")
#Graphic software for Atom IDE (figlet) introduced by Justin L. Downs

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a TCP/IP socket
#----------------------------------------------------------------------------------
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
    print("\nWelcome to Guess that Number!\n")

    return 0
#----------------------------------------------------------------------------------
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
                if data.decode() == "noFriends":
                    print("Waiting on a second player to join...")
                else:
                    amount_received += len(data)
                #print("received %s" % data.decode()) #UNCOMMENT FOR TESTING PURPOSES
            count+=1 ##Allow 25 loops without data before exiting loop

    except ConnectionResetError or ConnectionAbortedError:
        print("Your guess was not received before the game ended, sorry :-(...reconnect and try again")
        return
    return data.decode(), guess
#----------------------------------------------------------------------------------
def quitGuess():

    print("Thanks for playing!!! Closing Connection!")
    sock.close()
    return

#----------------------------------------------------------------------------------
def getvalidinput():
    """Requests a user input for the guess, converts to an integer for checking value is between 1-100, if
    not it prompts the user again, if it is in returns the valid response as a string for further use by
    the program."""

    notValidResponse = True

    while notValidResponse == True:

        try:
            response = int(input("\nWhat number would you like to guess? (### from 1-100): "))

            if (1 > response) or (response > 100):
                print("\nInvalid guess, please guess an integer from 1-100 in format ###\n")
                notValidResponse = True #Set variable back to true to prompt user for guess once more

            else: #Guess was good so exit the loop
                notValidResponse = False
        except: #If a user inputs a special character or letter prompt and allow loop to restart
            print("\nInvalid guess, please guess an integer from 1-100 in format ###\n")

    return str(response)
#----------------------------------------------------------------------------------
def checkWinner(message, guess):

    #Split the returned server string into a list at commas:
    results = message.split(',')

    #Check first value to see if win or lose
    if results[0] == '1':
        winOrLose='WIN!!!'
    elif results[0] =='2':
        winOrLose='LOSE:-(...'

    #Store answer returned by server:
    answer = results[1]

    #Store num of winners:
    num_win=results[2]

    #Store winning answer(s) sent by server:
    winAns = results[3] #First winning result

    #Check if more than one winner, concatenate answers in single string:
    if int(num_win)>1:
        for x in range(4,len(results)):
         winAns = winAns + ', ' + results[x]

    preface = "\nThe results are in... we have " + num_win + " winner(s)!"

    print(preface, 'YOU', winOrLose, "Here is the answer:", answer + ", and the winning guess(es):", winAns +'!\n')

    return

## MAIN PROGRAM:

connect2server()
win_mess,guess=guessSend()
checkWinner(win_mess, guess)
quitGuess()
