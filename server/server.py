import json
import socketserver

from DBHandler import DBHandler
from server_auth import ServerAuth
from server_msgs import ServerMsgs
from server_methods import ServerMethods

HOST, PORT = "localhost", 9999
METHODS = {
    ServerMethods.LOG_IN.value: ServerAuth.log_in,
    ServerMethods.SIGN_UP.value: ServerAuth.sign_up,
    ServerMethods.SEND_MESSAGE.value: ServerMsgs.send_msg,
    ServerMethods.RECEIVE_MESSAGES.value: ServerMsgs.get_msgs
}


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        request = json.loads(data.decode("utf-8"))
        request_type, request_body = request.popitem()
        response = METHODS[int(request_type)](request_body)
        if type(response) == list:
            response = [i.model_dump() for i in response]
            response = json.dumps(response)
        else:
            response = json.dumps(response.model_dump())
        self.request.sendall(bytes(response, "utf-8"))


if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
