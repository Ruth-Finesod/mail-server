from DBHandler import DBHandler
from communication_objects import Login, SignUp, GenericResponse, LogInResponse
from cookie_handler import CookieHandler
from hashlib import sha256
from typing import Dict


class ServerAuth:
    db = DBHandler()

    @classmethod
    def log_in(cls, request_data: Dict[str, str]) -> LogInResponse:
        request = Login(**request_data)
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        user = cls.db.query('users', {'email': request.email, 'password': hashed_password})
        if user:
            cookie = CookieHandler.sign(request.email + hashed_password)
            response_data = {'status': True, 'message': 'logged in successfully', 'cookie': cookie}
            response = LogInResponse(**response_data)
        else:
            response_data = {'status': False, 'message': 'login failed, username or password is incorrect',
                             'cookie': ''}
            response = LogInResponse(**response_data)
        return response

    @classmethod
    def sign_up(cls, request_data: Dict[str, str]) -> GenericResponse:
        request = SignUp(**request_data)
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        if not cls.db.query('users', {'email': request.email}):
            cls.db.write('users', {'email': request.email, 'password': hashed_password, 'name': request.full_name})
            response_data = {'status': True, 'message': 'successfully signed up'}
            response = GenericResponse(**response_data)
        else:
            response_data = {'status': True, 'message': 'username already exists'}
            response = GenericResponse(**response_data)
        return response
