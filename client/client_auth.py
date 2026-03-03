from typing import Tuple
from client_send import send
from server_methods import ServerMethods
from communication_objects import SignUp, Login, GenericResponse


class ClientAuth:

    def __init__(self, method: ServerMethods):
        self.email = ''
        self.password = ''
        self.cookie = b''
        if method == ServerMethods.LOG_IN:
            self.input_log_in()
        elif method == ServerMethods.SIGN_UP:
            self.input_sign_up()

    def input_log_in(self):
        self.email = input('email address: ')
        self.password = input('password: ')
        self.send_log_in()

    def send_log_in(self):
        request_data = {'email': self.email, 'password': self.password}
        request_body = Login(**request_data)
        request = {ServerMethods.LOG_IN: request_body.model_dump()}
        response = GenericResponse(**send(request))
        if response.status:
            self.cookie = response.message
        else:
            print(response.message)
            self.input_log_in()

    def input_sign_up(self):
        self.email = input('email address: ')
        name = input('full name: ')
        self.password = input('password: ')
        repeat_password = input('repeat password: ')
        if not self.password_validation(repeat_password):
            self.send_sign_up(name)

    def send_sign_up(self, name):
        request_data = {'email': self.email, 'name': name, 'password': self.password}
        request_body = SignUp(**request_data)
        request = {ServerMethods.SIGN_UP: request_body.model_dump()}
        response = GenericResponse(**send(request))
        print(response.message)
        if response.status:
            self.send_log_in()
        else:
            self.input_sign_up()

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
