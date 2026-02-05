from socket import *
import argparse

CHUNK_SIZE = 1024

# receive file content from the connected TCP socket and save to filename
def recv_to_file(connectionSocket, filename: str) -> None:
    with open(filename, "wb") as f:
        while True:
            data = connectionSocket.recv(CHUNK_SIZE)
            if not data:
                break
            f.write(data)

# ACTV mode
def do_actv(server_addr: str, n_port: int, filename: str) -> None:
    # destination client in stage 2 
    # client listens, server connects back
    listenSocket = socket(AF_INET, SOCK_STREAM)
    try:
        # bind socket to a free port
        listenSocket.bind(("", 0))
        
        # listen for server TCP connection request
        listenSocket.listen(1)

        # get listen socket port number
        r_port = listenSocket.getsockname()[1]
        print(f"R_PORT={str(r_port)}")

        # Stage 1 - UDP negotiation
        negotiationSocket = socket(AF_INET, SOCK_DGRAM)
        try:
            # GET <filename> <r_port>
            negotiationSocket.sendto(f"GET {filename} {r_port}".encode(), (server_addr, n_port))
            # get server response
            response, _ = negotiationSocket.recvfrom(CHUNK_SIZE)
        finally:
            negotiationSocket.close()
            
        text = response.decode().strip()
        if text == "404 Not Found":
            return

        # server initiates TCP connection to client listening port
        connectionSocket, _ = listenSocket.accept()
        
        # save the file
        try:
            recv_to_file(connectionSocket, filename)
        finally:
            connectionSocket.close()
    finally:
        listenSocket.close()

# PASV mode
def do_pasv(server_addr: str, n_port: int, filename: str) -> None:
    # Stage 1 - UDP Negotiation
    negotiationSocket = socket(AF_INET, SOCK_DGRAM)
    try:
        ## GET <filename> PASV
        negotiationSocket.sendto(f"GET {filename} PASV".encode(), (server_addr, n_port))
        # get the server response
        response, _ = negotiationSocket.recvfrom(CHUNK_SIZE)
    finally:
        negotiationSocket.close()
        
    text = response.decode().strip()
    if text == "404 Not Found":
        return

    # get the TCP server port number
    r_port = int(text)

    # Stage 2 - TCP transaction
    receiverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        # client connects to TCP server and save file
        receiverSocket.connect((server_addr, r_port))
        recv_to_file(receiverSocket, filename)
    finally:
        receiverSocket.close()

def main() -> None:
    # get the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("serverAddress")
    parser.add_argument("n_port", type=int)
    parser.add_argument("mode", choices=["PASV", "ACTV"])
    parser.add_argument("filename")
    args = parser.parse_args()

    if args.mode == "PASV":
        do_pasv(args.serverAddress, args.n_port, args.filename)
    else:
        do_actv(args.serverAddress, args.n_port, args.filename)


if __name__ == "__main__":
    main()
