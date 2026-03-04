from DBHandler import DBHandler
from communication_objects import Login, SignUp, GenericResponse, LogInResponse
from cookie_handler import CookieHandler
import json
from typing import Dict


class ServerAuth:
    def __init__(self, db: DBHandler):
        self.db = db

    def log_in(self, request_data: Dict[str, str]) -> LogInResponse:
        request = Login(**request_data)
        hashed_password = hash(request.password)
        user = self.db.query('users', {'email': request.email})
        if user:
            cookie = CookieHandler.sign(request.email + str(hashed_password))
            response_data = {'status': True, 'message': 'logged in successfully', 'cookie': cookie}
            response = LogInResponse(**response_data)
        else:
            response_data = {'status': False, 'message': 'login failed, username or password is incorrect',
                             'cookie': ''}
            response = LogInResponse(**response_data)
        return response

    def sign_up(self, request_data: Dict[str, str]) -> GenericResponse:
        request = SignUp(**request_data)
        hashed_password = hash(request.password)
        if not self.db.query('users', {'email': request.email}):
            self.db.write('users', {'email': request.email, 'password': hashed_password, 'name': request.name})
            response_data = {'status': True, 'message': 'successfully signed up'}
            response = GenericResponse(**response_data)
        else:
            response_data = {'status': True, 'message': 'username already exists'}
            response = GenericResponse(**response_data)
        return response
