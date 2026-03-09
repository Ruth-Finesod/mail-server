import json
import socket
from typing import Dict, Any

HOST, PORT = "localhost", 9999
MESSAGE_END_MAGIC = b'RfSk\n'


def send(data: Dict[int, Any]) -> Dict[str, Any]:
    """
    Send data to server
    :param data: the request from the server
    :return: the response from the server
    """
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        data = json.dumps(data)
        sock.sendall(bytes(data, "utf-8") + MESSAGE_END_MAGIC)
        # Receive data from the server and shut down
        received = sock.recv(2000)
        received = json.loads(received)
    return received
