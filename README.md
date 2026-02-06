# UDP-TCP-File-Transfer-Client-Server
A lightweight file transfer system implemented in Python using low-level socket programming. The application follows a simplified FTP-style protocol where a client requests files from a server using UDP for negotiation and TCP for reliable data transfer.

The system supports passive and active connection mode, enabling dynamic negotiation of data ports before transferring file contents between client and server.

## Features
- UDP-based negotiation protocol
- TCP-based reliable file transfer
- Passive transfer mode support
- Automatic port negotiation

## System Overview
The transfer process occurs in two stages:
1. Negotiation stage (UDP)
The client sends a request specifying the file and transfer mode.
The server responds with a dynamically allocated TCP port for data transfer.
2. Transaction stage (TCP)
The client connects to the server on the negotiated port and downloads the file contents.

## Usage
Start the server
```./server.sh <storage_directory>```

The server prints the negotiation port:
```SERVER_PORT=<n_port>```

Run the client
```./client.sh <server_address> <n_port> [PASV|ACTV] <filename>```

Example:
```./client.sh 127.0.0.1 51234 PASV hello.txt```

The requested file will be downloaded to the client’s working directory.

## Files Included
- `server.py` – File transfer server
- `client.py` – File transfer client
- `server.sh` – Script to start the server
- `client.sh` – Script to start the client
- `storage/` – Directory containing files served to clients

## Testing Instructions
The program was built and tested on the University of Waterloo undergraduate environment.
Tested with:
- Python 3.x
- Example machines used:
    - ubuntu2404-002.student.cs.uwaterloo.ca
    - ubuntu2404-004.student.cs.uwaterloo.ca

Two shell scripts are provided to start the server and client.
Make scripts executable if needed:
```chmod +x server.sh client.sh```
Ensure Python 3 is installed before running the scripts: `python3 --version`

### Single Machine Testing
1. Start server: `./server.sh ./storage`   -> Server prints `SERVER_PORT=<n_port>`
2. Test Passive (PASV) mode:
    Run the client `./client.sh <server_address> <n_port> PASV <filename>`. Since the server and the client are running in the same system, 127.0.0.1 or localhost can be used as the server address.
    
    Expected behavior: 
    - If the file exists in the directory:
        a. Server prints a TCP port `R_PORT=<r_port>` for transfer 
        b. File is downloaded in client directory. Client exits quietly -> You can use `diff hello.txt storage/hello.txt` to verify the file content
    - If the file doesn't exist in the directory: client exits, server stays alive, no files are downloaded.

3. Test Active (ACTV) mode:
    Run the client `./client.sh <server_address> <n_port> ACTV <filename>`. Since the server and the client are running in the same system, 127.0.0.1 or localhost can be used as the server address.

    Expected behavior: 
    - If the file exists in the directory:
        a. Client prints a TCP listening port `R_PORT=<r_port>` for server to connect 
        b. File is downloaded in client directory. Client exits quietly -> You can use `diff hello.txt storage/hello.txt` to verify the file content
    - If the file doesn't exist in the directory: Client prints its listening port `R_PORT=<r_port>`, then exits after receiving 404 from the server. The server stays alive, no files are downloaded.

### Two Different Machine Testing
Run server and client on different machines. Suppose we use machine `ubuntu2404-002.student.cs.uwaterloo.ca` for server and `ubuntu2404-004.student.cs.uwaterloo.ca` for client
1. SSH into `ubuntu2404-002.student.cs.uwaterloo.ca` and run the server `./server.sh ./storage`   -> Server prints `SERVER_PORT=<n_port>`
2. SSH into the different host `ubuntu2404-004.student.cs.uwaterloo.ca` for client
3. Test Passive (PASV) mode:
    Run the client `./client.sh <server_address> <n_port> PASV <filename>`. In this case, server_address is `ubuntu2404-002.student.cs.uwaterloo.ca`

    Expected behavior: 
    - If the file exists in the directory:
        a. Server prints a TCP port `R_PORT=<r_port>` for transfer
        b. File is downloaded in client directory. Client exits quietly -> You can use `diff hello.txt storage/hello.txt` to verify the file content
    - If the file doesn't exist in the directory: client exits, server stays alive, no files are downloaded.

4. Test Active (ACTV) mode:
    Run the client `./client.sh <server_address> <n_port> ACTV <filename>`. In this case, server_address is `ubuntu2404-002.student.cs.uwaterloo.ca`

    Expected behavior: 
    - If the file exists in the directory:
        a. Client prints a TCP listening port `R_PORT=<r_port>` for server to connect 
        b. File is downloaded in client directory. Client exits quietly -> You can use `diff hello.txt storage/hello.txt` to verify the file content
    - If the file doesn't exist in the directory: Client prints its listening port `R_PORT=<r_port>`, then exits after receiving 404 from the server. The server stays alive, no files are downloaded.

## Technologies Used
- Python 3
- UDP sockets
- TCP sockets
- Client–server architecture

More details about the program:
[2026W CS456 Assignment 1.pdf](https://github.com/user-attachments/files/25076242/2026W.CS456.Assignment.1.pdf)

