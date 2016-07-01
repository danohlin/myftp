##@author Dan Ohlin
##Class: TCN-5030 Computer Communications and Networking Technologies
##Project 1
##due April 11, 2014

import sys
import os
from socket import *

if len(sys.argv) > 1:
    serverName = sys.argv[1]
serverPort = 21

#open connection to ftp server and login
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
response = clientSocket.recv(1024)
print response
user = raw_input('User: ')
commandToSend = 'USER ' + user + '\r\n'
clientSocket.send(commandToSend)
response = clientSocket.recv(1024)
print response
password = raw_input('Password: ')
commandToSend = 'PASS ' + password + '\r\n'
clientSocket.send(commandToSend)
response = clientSocket.recv(1024)
print response
address, dataPort = clientSocket.getsockname()

while True:

    command = raw_input('ftp> ') #prompt user for ftp command

    if command.upper() == 'QUIT': #close ftp connection and quit program
        commandToSend = 'QUIT\r\n'
        clientSocket.send(commandToSend)
        response = clientSocket.recv(1024)
        print response
        clientSocket.close()
        quit()

    if command[0:3].upper() == 'CD ': #change to directory specified
        commandToSend = 'CWD ' + command[3:] + '\r\n'
        clientSocket.send(commandToSend)
        response = clientSocket.recv(1024)
        print response

    if command[0:6].upper() == 'DELETE': #delete file specified
        commandToSend = 'DELE ' + command[7:] + '\r\n'
        clientSocket.send(commandToSend)
        response = clientSocket.recv(1024)
        print response
        
    if command.upper() == 'PWD': #get current working directory
        commandToSend = 'XPWD\r\n'
        clientSocket.send(commandToSend)
        response = clientSocket.recv(1024)
        print response

    if command.upper() == 'LS': #list files/folder in current directory
        dataPort += 1

        availablePort = False 
        while availablePort == False: #see if local port is available, if not try another port
            try:
                dataSocket = socket(AF_INET,SOCK_STREAM)
                dataSocket.bind(('',dataPort))
                availablePort = True
            except error:
                dataPort += 1
        
        lDataPort = str(int(hex(dataPort)[2:4], 16))
        rDataPort = str(int(hex(dataPort)[4:6], 16))
        arrayAddress = str.split(address, ".")

        commandToSend = 'PORT ' + arrayAddress[0] + "," + arrayAddress[1] + "," + arrayAddress[2] + "," + arrayAddress[3] + "," + lDataPort + ',' + rDataPort + '\r\n'
        clientSocket.send(commandToSend) #send port command, telling ftp server which local host port to connect to
        lsResponse = clientSocket.recv(1024)
        print lsResponse

        commandToSend = 'NLST\r\n' #list files/folders ftp command
        clientSocket.send(commandToSend)

        dataSocket.listen(1)
        dataConn, addr = dataSocket.accept()
       
        nlstResponse = clientSocket.recv(1024)
        print nlstResponse

        listing = dataConn.recv(1024)
        print listing
        dataConn.close()
        nlstResponse = clientSocket.recv(1024)
        print nlstResponse
        dataSocket.close()


    if command[0:3].upper() == 'PUT': #transfer file to ftp server
        dataPort += 1

        availablePort = False
        while availablePort == False:
            try:
                dataSocket = socket(AF_INET,SOCK_STREAM)
                dataSocket.bind(('',dataPort))
                availablePort = True
            except error:
                dataPort += 1
        
        lDataPort = str(int(hex(dataPort)[2:4], 16))
        rDataPort = str(int(hex(dataPort)[4:6], 16))
        arrayAddress = str.split(address, ".")
        commandToSend = 'PORT ' + arrayAddress[0] + "," + arrayAddress[1] + "," + arrayAddress[2] + "," + arrayAddress[3] + "," + lDataPort + ',' + rDataPort + '\r\n'
        clientSocket.send(commandToSend)
        putResponse = clientSocket.recv(1024)
        print putResponse

        commandToSend = 'STOR ' + command[4:] + '\r\n' #send file transfer command
        clientSocket.send(commandToSend)

        dataSocket.listen(1)
        dataConn, addr = dataSocket.accept()
        
        storResponse = clientSocket.recv(1024)
        print storResponse

        f = open(command[4:]) #open file and transfer it
        transferFile = f.read()
        for i in range(0, len(transferFile)):
            dataConn.send(transferFile[i])
        f.close()

        dataConn.close()
        storResponse = clientSocket.recv(1024)
        print storResponse
        dataSocket.close()
        size = os.path.getsize(command[4:])
        print 'ftp: Successful file transfer. ' + str(size) + ' byte(s) transfered'

    if command[0:3].upper() == 'GET': #get file from ftp server
        dataPort += 1

        availablePort = False
        while availablePort == False:
            try:
                dataSocket = socket(AF_INET,SOCK_STREAM)
                dataSocket.bind(('',dataPort))
                availablePort = True
            except error:
                dataPort += 1
        
        lDataPort = str(int(hex(dataPort)[2:4], 16))
        rDataPort = str(int(hex(dataPort)[4:6], 16))
        arrayAddress = str.split(address, ".")
        commandToSend = 'PORT ' + arrayAddress[0] + "," + arrayAddress[1] + "," + arrayAddress[2] + "," + arrayAddress[3] + "," + lDataPort + ',' + rDataPort + '\r\n'
        clientSocket.send(commandToSend)
        getResponse = clientSocket.recv(1024)
        print getResponse

        commandToSend = 'RETR ' + command[4:] + '\r\n' #send get file command to ftp server
        clientSocket.send(commandToSend)

        dataSocket.listen(1)
        dataConn, addr = dataSocket.accept()
        
        retrResponse = clientSocket.recv(1024)
        print retrResponse

        receiveFile = dataConn.recv(1024) #receive file
        f = open(command[4:], 'w') #open and write file locally
        for line in receiveFile:
            f.write(line)
        f.close()

        dataConn.close()
        retrResponse = clientSocket.recv(1024)
        print retrResponse
        dataSocket.close()
        size = os.path.getsize(command[4:])
        print 'ftp: Successful file transfer. ' + str(size) + ' byte(s) received'
