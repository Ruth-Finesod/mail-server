import socket
from typing import Dict

HOST, PORT = "localhost", 9999


def send(data: Dict[str, str]) -> bool:
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
        sock.sendall(b"\n")
        # Receive data from the server and shut down
        received = bool(sock.recv(1024), "utf-8")

    print("Sent:    ", data)
    print("Received:", received)
    return received
