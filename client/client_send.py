import json
import socket
import struct
from typing import Dict, Any

HOST, PORT = "localhost", 9999


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
        data = json.dumps(data).encode("utf-8")
        length = struct.pack(">I", len(data))
        sock.sendall(length + data)
        # Receive data from the server and shut down
        resp_len = struct.unpack(">I", sock.recv(4))[0]
        resp_data = b''
        while len(resp_data) != resp_len:
            resp_data += sock.recv(resp_len - len(resp_data))
        received = json.loads(resp_data.decode("utf-8"))
    return received
