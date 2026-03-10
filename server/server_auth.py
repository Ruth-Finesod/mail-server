from hashlib import sha256

from DBHandler import DBHandler
from communication_objects import Login, SignUp
from errors import *


class ServerAuth:
    USERS_TABLE = 'users'

    @classmethod
    def log_in(cls, request: Login) -> str:
        """
        checks is the user in the request_data exists
        :param request: Login object
        :return: message string or errors
        """
        db = DBHandler()
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        user = db.query(cls.USERS_TABLE, {'email': request.email, 'password': hashed_password})
        if not user:
            raise BadRequestError('login failed, username or password is incorrect')
        db.close()
        return 'logged in successfully'

    @classmethod
    def sign_up(cls, request: SignUp) -> str:
        """
        signs up a new user by writing it to the db and then logging in
        :param request: SignUp object
        :return: message string or errors
        """
        db = DBHandler()
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        if db.query(cls.USERS_TABLE, {'email': request.email}):
            db.close()
            raise BadRequestError('username already exists')
        db = DBHandler()
        db.write(cls.USERS_TABLE, {'email': request.email, 'password': hashed_password, 'name': request.full_name})
        db.close()
        return 'successfully signed up'
