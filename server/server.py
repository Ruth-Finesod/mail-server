import json
import socketserver
from server_methods import ServerMethods
from server_auth import ServerAuth
from DBHandler import DBHandler

HOST, PORT = "localhost", 9999
AUTH_METHODS = [ServerMethods.LOG_IN.value, ServerMethods.SIGN_UP.value]
MSGS_METHODS = [ServerMethods.SEND_MESSAGE.value, ServerMethods.RECEIVE_MESSAGES.value]


class MyTCPHandler(socketserver.BaseRequestHandler):
    dbhandler = DBHandler()

    def handle(self):
        data = self.request.recv(1024)
        request = json.loads(data.decode("utf-8"))
        request_type, request_body = request.popitem()
        if int(request_type) in AUTH_METHODS:
            a = ServerAuth(self.dbhandler)
            if int(request_type) == ServerMethods.LOG_IN.value:
                response = a.log_in(request_body)
            elif int(request_type) == ServerMethods.SIGN_UP.value:
                response = a.sign_up(request_body)
        response = json.dumps(response.model_dump())
        self.request.sendall(bytes(response, "utf-8"))


if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
