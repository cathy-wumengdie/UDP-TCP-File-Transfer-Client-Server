import os
from socket import *
import argparse

CHUNK_SIZE = 1024

# read the file and send its content to client
def send_file(transactionSocket, fullpath: str) -> None:
    with open(fullpath, "rb") as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            transactionSocket.sendall(chunk)
            chunk = f.read(CHUNK_SIZE)

# ACTV mode
def do_actv(r_port: int, clientIP: str, fullpath: str) -> None:
    # create a TCP socket
    transactionSocket = socket(AF_INET, SOCK_STREAM)
    
    # initiates a TCP connection to the client
    transactionSocket.connect((clientIP, r_port))
    
    # send file content and close TCP socket, return to negotiation stage
    send_file(transactionSocket, fullpath)
    transactionSocket.close()
    
    
# PASV mode
def do_pasv(negotiationSocket, clientAddress, fullpath: str) -> None:
    # create a TCP socket
    connectionSocket = socket(AF_INET, SOCK_STREAM)
        
    # bind socket to a free port number
    connectionSocket.bind(("", 0))
        
    # get the TCP server port number
    _, r_port = connectionSocket.getsockname()
    print("R_PORT=" + str(r_port))
        
    # listen for client TCP connection request
    connectionSocket.listen(1)
        
    # send the port number to client
    response = str(r_port)
    negotiationSocket.sendto(response.encode(), clientAddress)
        
    # wait for client connection, new socket created upon connection
    transactionSocket, _ = connectionSocket.accept()
            
    send_file(transactionSocket, fullpath)
                    
    # close TCP sockets, return to negotiation stage
    transactionSocket.close()
    connectionSocket.close()

def main() -> None:
    # get the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("storageDirectory")
    storageDirectory = parser.parse_args().storageDirectory
    
    # create a UDP socket
    negotiationSocket = socket(AF_INET, SOCK_DGRAM)
    
    # bind socket to a free port number
    negotiationSocket.bind(("", 0))

    # get the server address and port number
    _, n_port = negotiationSocket.getsockname()
    print("SERVER_PORT=" + str(n_port))

    # Stage 1 - UDP Negotiation
    # wait for client requests
    while True:
        # get the filename and mode
        request, clientAddress = negotiationSocket.recvfrom(CHUNK_SIZE)
        parts = request.decode().split()
        if len(parts) == 3:
            filename = parts[1]
            mode_or_r_port = parts[2]
        else:
            continue

        # get the full path and check if the file exists
        fullpath = os.path.join(storageDirectory, filename)
        isExist = os.path.isfile(fullpath)
    
        if not isExist:
            response = "404 Not Found"
            negotiationSocket.sendto(response.encode(), clientAddress)
            continue
        
        # Stage 2 - TCP Transcation
        if mode_or_r_port == "PASV":
            do_pasv(negotiationSocket, clientAddress, fullpath)
        else:
            # repond to client with 200 OK
            response = "200 OK"
            negotiationSocket.sendto(response.encode(), clientAddress)
            clientIP = clientAddress[0]
            # mode is ACTV, pass in r_port as int
            do_actv(int(mode_or_r_port), clientIP, fullpath)


if __name__ == "__main__":
    main()