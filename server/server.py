import json
import socketserver
from server_methods import ServerMethods
from server_auth import ServerAuth
from DBHandler import DBHandler

HOST, PORT = "localhost", 9999
AUTH_METHODS = [ServerMethods.LOG_IN, ServerMethods.SIGN_UP]
MSGS_METHODS = [ServerMethods.SEND_MESSAGE, ServerMethods.RECEIVE_MESSAGES]


class MyTCPHandler(socketserver.BaseRequestHandler):
    auth_dbhandler = DBHandler('path')

    def handle(self):
        data = self.request.recv(1024)
        request = json.loads(data.decode("utf-8"))
        request_type, request_body = request.popitem()
        if request_type in AUTH_METHODS:
            a = ServerAuth(self.auth_dbhandler)
            if request_type == ServerMethods.LOG_IN:
                response = a.log_in(request_body)
            elif request_type == ServerMethods.SIGN_UP:
                response = a.sign_up(request_body)
        response = json.dumps(response)
        self.request.sendall(response)


if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
