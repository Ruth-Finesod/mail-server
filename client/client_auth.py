from base_client_class import BaseClass
from client_send import send
from communication_objects import SignUp, Login, GenericResponse, LogInResponse
from server_methods import ServerMethods


class ClientAuth(BaseClass):
    CHOICES = {
        'l': 'log_in',
        's': 'sign_up'
    }

    def __init__(self):
        self.email = ''
        self.password = ''
        self.cookie = ''
        self.pick_method()

    def _body_request(self):
        return {'email': self.email, 'password': self.password}

    def log_in(self):
        """
        get input for log in
        """
        self.email = input('email address: ')
        self.password = input('password: ')
        self.send_log_in(self._body_request())

    def send_log_in(self, request_data):
        """
        send log in parms to server in a Login format
        :param request_data: log in parms
        get cookie from server
        print message from server
        """
        request = {ServerMethods.LOG_IN.value: Login(**request_data).model_dump()}
        response = send(request)
        response = LogInResponse(**response)
        print(response.message)
        if response.status:
            self.cookie = response.cookie
        else:
            self.log_in()

    def sign_up(self):
        """
        get input for sign up
        """
        self.email = input('email address: ')
        full_name = input('full name: ')
        self.password = input('password: ')
        repeat_password = input('repeat password: ')
        if self.password_validation(repeat_password):
            self.send_sign_up(full_name, self._body_request())
        else:
            self.sign_up()

    def send_sign_up(self, full_name, request_data):
        """
        send sign up to parms to server in a SignUp format
        :param full_name: full name
        :param request_data: other sign up parms
        get and print message from server
        """
        request = {ServerMethods.SIGN_UP.value: SignUp(full_name=full_name, **request_data).model_dump()}
        response = send(request)
        response = GenericResponse(**response)
        print(response.message)
        if response.status:
            self.send_log_in(self._body_request())
        else:
            self.sign_up()

    def password_validation(self, repeat_password: str) -> bool:
        """
        validate the password
        :param repeat_password: the repeated password
        :return: if password is valid
        """
        if self.password != repeat_password:
            print('passwords not match')
        elif len(self.password) < 8:
            print('password must be at least 8 characters')
        elif self.password.isnumeric() or self.password.isalpha():
            print('password must have numbers and letters')
        elif self.password.islower() or self.password.isupper():
            print('password must have both uppercase and lowercase characters')
        else:
            return True
        return False
