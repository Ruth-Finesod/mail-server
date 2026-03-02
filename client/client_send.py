import socket
from server_methods import ServerMethods
from typing import Dict
import json

HOST, PORT = "localhost", 9999


def send(data: Dict[ServerMethods, Dict[str, str]]) -> str:
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        data = json.dumps(data)
        sock.sendall(bytes(data, "utf-8"))
        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
    return received
