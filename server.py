import os
from socket import *
import argparse

## get the command line argument
parser = argparse.ArgumentParser()
parser.add_argument("storageDirectory")
storageDirectory = parser.parse_args().storageDirectory

## create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

## bind socket to a free port number
serverSocket.bind(("", 0))

## get the server address and port number
(serverAddress, n_port) = serverSocket.getsockname()
print("SERVER_PORT=" + str(n_port))

## Stage 1 - Negotiation
## wait for client requests
while True:
    ## get the filename and mode
    request, clientAddress = serverSocket.recvfrom(2048)
    parts = request.decode().split()
    filename = parts[1]
    mode = parts[2]
    
    ## get the full path and check if the file exists
    fullpath = os.path.join(storageDirectory, filename)
    isExist = os.path.isfile(fullpath)
    
    if not isExist:
        response = "404 Not Found"
        serverSocket.sendto(response.encode(), clientAddress)
    else:
        ## Stage 2 - Transcation
        ## create a TCP socket
        


