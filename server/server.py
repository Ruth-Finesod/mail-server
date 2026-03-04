import socketserver
import json
from datetime import datetime
from typing import Tuple

HOST, PORT = "localhost", 9999
USERS_PATH = "json files/users.json"
MSGS_PATH = "json files/messages.json"
USER_PARMS = ['username', 'password', 'last_read']

class MyTCPHandler(socketserver.BaseRequestHandler):


    def handle(self):
        data = self.request.recv(1024)
        print(f"Received from {self.client_address[0]}:")
        request_dict = json.loads(data.decode("utf-8"))
        for func_name, kwargs in request_dict:
            code, msg = exec(f"self.{func_name}(**{kwargs})")
            self.request.sendall(b'{code}{msg}')

    @staticmethod
    def get_user(username: str):
        users = json.load(open(USERS_PATH, "r"))
        for user in users:
            if user["username"] == username:
                return user
        return None

    def server_sign_up(self, username, hashed_password):
        if not self.get_user(username):
            users = json.load(open(USERS_PATH, "r"))
            users.append(zip(USER_PARMS, [username, hashed_password, datetime.today()]))
            json.dump(users, open(USERS_PATH, "w"))
            return 1, 'successfully signed up'
        else:
            return 0, 'username already exists'

    def server_login(self, username: str, hashed_password: str):
        user = self.get_user(username)
        if user:
            if user["password"] == hashed_password:
                return 1, 'logged in successfully'
            else:
                return 0, 'login failed, password is incorrect'
        else:
            return 0, 'login failed, username does not exist'

    def server_send_msgs(self, username):
        user = self.get_user(username)

if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
