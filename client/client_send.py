import json
import socket
import struct
from typing import Dict, Any

HOST, PORT = "localhost", 9999


def socket_receive(sock, length: int):
    data = b''
    while len(data) != length:
        data += sock.recv(length - len(data))
    return data


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
        resp_len = struct.unpack(">I", socket_receive(sock, 4))[0]
        received = json.loads(socket_receive(sock, resp_len).decode("utf-8"))
    return received
