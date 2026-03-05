from hashlib import sha256
from typing import Dict

from DBHandler import DBHandler
from communication_objects import Login, SignUp, GenericResponse, LogInResponse
from cookie_handler import CookieHandler


class ServerAuth:
    db = DBHandler()
    USERS_TABLE = 'users'

    @classmethod
    def log_in(cls, request_data: Dict[str, str]) -> LogInResponse:
        """
        checks is the user in the request_data exists and makes a cookie
        :param request_data: dict of strings in the format of Login object
        :return: in the format of LogInResponse, if logged returns success and the cookie created, if not returns failure
        """
        request = Login(**request_data)
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        user = cls.db.query(cls.USERS_TABLE, {'email': request.email, 'password': hashed_password})
        if user:
            cookie = CookieHandler.sign(request.email + request.password)
            response_data = {'status': True, 'message': 'logged in successfully', 'cookie': cookie}
            response = LogInResponse(**response_data)
        else:
            response_data = {'status': False, 'message': 'login failed, username or password is incorrect',
                             'cookie': ''}
            response = LogInResponse(**response_data)
        return response

    @classmethod
    def sign_up(cls, request_data: Dict[str, str]) -> GenericResponse:
        """
        signs up a new user by writing it to the db and then logging in
        :param request_data: dict of strings with information of the user in the format of SignUp object
        :return: in the format of GenericResponse, if logged returns success if not returns failure
        """
        request = SignUp(**request_data)
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        if not cls.db.query(cls.USERS_TABLE, {'email': request.email}):
            cls.db.write(cls.USERS_TABLE, {'email': request.email, 'password': hashed_password, 'name': request.full_name})
            response_data = {'status': True, 'message': 'successfully signed up'}
            response = GenericResponse(**response_data)
        else:
            response_data = {'status': True, 'message': 'username already exists'}
            response = GenericResponse(**response_data)
        return response
