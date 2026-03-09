from hashlib import sha256
from typing import Dict

from DBHandler import DBHandler
from communication_objects import Login, SignUp, GenericResponse, LogInResponse


class ServerAuth:
    db = DBHandler()
    USERS_TABLE = 'users'

    @classmethod
    def log_in(cls, request: Login) -> LogInResponse:
        """
        checks is the user in the request_data exists
        :param request: Login object
        :return: in the format of LogInResponse, if logged returns success, if not returns failure
        """
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        user = cls.db.query(cls.USERS_TABLE, {'email': request.email, 'password': hashed_password})
        if user:
            response_data = {'status': True, 'message': 'logged in successfully'}
            response = LogInResponse(**response_data)
        else:
            response_data = {'status': False, 'message': 'login failed, username or password is incorrect'}
            response = LogInResponse(**response_data)
        return response

    @classmethod
    def sign_up(cls, request: SignUp) -> GenericResponse:
        """
        signs up a new user by writing it to the db and then logging in
        :param request: SignUp object
        :return: in the format of GenericResponse, if logged returns success if not returns failure
        """
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        if not cls.db.query(cls.USERS_TABLE, {'email': request.email}):
            cls.db.write(cls.USERS_TABLE, {'email': request.email, 'password': hashed_password, 'name': request.full_name})
            response_data = {'status': True, 'message': 'successfully signed up'}
            response = GenericResponse(**response_data)
        else:
            response_data = {'status': True, 'message': 'username already exists'}
            response = GenericResponse(**response_data)
        return response
