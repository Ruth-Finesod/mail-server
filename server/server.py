import json
import socketserver
from typing import Any

from pydantic import BaseModel

from server_auth import ServerAuth
from server_methods import ServerMethods
from server_msgs import ServerMsgs

HOST, PORT = "localhost", 9999
METHODS = {
    ServerMethods.LOG_IN.value: ServerAuth.log_in,
    ServerMethods.SIGN_UP.value: ServerAuth.sign_up,
    ServerMethods.SEND_MESSAGE.value: ServerMsgs.send_msg,
    ServerMethods.RECEIVE_MESSAGES.value: ServerMsgs.get_msgs,
    ServerMethods.READ_MSG.value: ServerMsgs.read_msg
}
MESSAGE_END_MAGIC = b'RfSk\n'

def make_jsonable(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return make_jsonable(obj.model_dump())
    if isinstance(obj, dict):
        return {k: make_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [make_jsonable(v) for v in obj]
    return obj


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        pieces = [b'']
        while not pieces[-1].endswith(MESSAGE_END_MAGIC):
            pieces.append(self.request.recv(2000))
        data = b''.join(pieces)
        data = data[:-len(MESSAGE_END_MAGIC)]
        """receives data from the client, put in the correct method, and sends the response"""
        request = json.loads(data.decode("utf-8"))
        request_type, request_body = request.popitem()
        response = METHODS[int(request_type)](request_body)
        response = json.dumps(make_jsonable(response))
        self.request.sendall(bytes(response, "utf-8"))


if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
