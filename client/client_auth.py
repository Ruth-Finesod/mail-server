from typing import Tuple
from client_send import send
from server_methods import ServerMethods


class ClientAuth:

    def __init__(self, method: ServerMethods):
        self.email = ''
        self.password = ''
        self.cookie = b''
        if method == ServerMethods.LOG_IN:
            self.log_in()
        elif method == ServerMethods.SIGN_UP:
            self.sign_up()

    def log_in(self):
        self.email = input('email address: ')
        self.password = input('password: ')
        request = {ServerMethods.LOG_IN: {'email': self.email, 'password': self.password}}
        response = send(request)
        flag, message = response[0], response[1:]
        if flag == b'1':
            self.cookie = message
        else:
            print(message)
            self.log_in()

    def sign_up(self):
        self.email = input('email address: ')
        name = input('full name: ')
        self.password = input('password: ')
        repeat_password = input('repeat password: ')
        if not self.password_validation(repeat_password):
            self.sign_up()
        request = {ServerMethods.SIGN_UP: {'email': self.email, 'name': name, 'password': self.password}}
        response = send(request)
        flag, message = response[0], response[1:]
        print(message)
        if flag == b'1':
            self.log_in()
        else:
            self.sign_up()

    def password_validation(self, repeat_password: str) -> bool:
        if self.password != repeat_password:
            print('passwords not match')
        elif len(self.password) < 8:
            print('password must be at least 8 characters')
        elif self.password.islower():
            print('password must have at least one uppercase character')
        # more checks
        else:
            return True
        return False


def authenticate() -> ClientAuth:
    method = pick_method()
    user = ClientAuth(method)
    return user


def pick_method() -> ServerMethods:
    print('how would you like to authenticate?')
    choices = {'l': ServerMethods.LOG_IN, 's': ServerMethods.SIGN_UP}
    choice = input('l: log in\ns: sign up\nyour choice: ')
    picked_method = choices.get(choice)
    if picked_method:
        return picked_method
    else:
        print('you must pick one of the presented options')
        return pick_method()
