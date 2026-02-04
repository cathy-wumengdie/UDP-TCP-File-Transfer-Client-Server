# UDP-TCP-File-Transfer-Client-Server
A lightweight file transfer system implemented in Python using low-level socket programming. The application follows a simplified FTP-style protocol where a client requests files from a server using UDP for negotiation and TCP for reliable data transfer.

The system supports passive connection mode, enabling dynamic negotiation of data ports before transferring file contents between client and server.

# Features
- UDP-based negotiation protocol
- TCP-based reliable file transfer
- Passive transfer mode support
- Automatic port negotiation

# System Overview
The transfer process occurs in two stages:
1. Negotiation stage (UDP)
The client sends a request specifying the file and transfer mode.
The server responds with a dynamically allocated TCP port for data transfer.
2. Transaction stage (TCP)
The client connects to the server on the negotiated port and downloads the file contents.

# Usage
Start the server
```./server.sh <storage_directory>```

The server prints the negotiation port:
```SERVER_PORT=<port>```

Run the client
```./client.sh <server_address> <n_port> PASV <filename>```

Example:
```./client.sh 127.0.0.1 51234 PASV hello.txt```

The requested file will be downloaded to the client’s working directory.

# Technologies Used
- Python
- UDP sockets
- TCP sockets
- Client–server architecture

