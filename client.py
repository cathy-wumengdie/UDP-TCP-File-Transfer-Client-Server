from socket import *
import argparse

## get the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("serverAddress")
parser.add_argument("n_port")
parser.add_argument("mode")
parser.add_argument("filename")
args = parser.parse_args()

## create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

## Stage 1 - Negotiation
## attach server name and port number, send GET request into socket
clientSocket.sendto(
    ("GET " + args.filename + " " + args.mode).encode(), (args.serverAddress, args.n_port)
)

## get the response from server
response, serverAddress = clientSocket.recvfrom(1024)

if response is "404 Not Found":
    clientSocket.close()
else:
    ## Stage 2 - Transcation




