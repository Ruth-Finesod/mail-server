from DBHandler import DBHandler
from communication_objects import SendMsg, GetMsg, GenericResponse, MsgResponse
from cookie_handler import CookieHandler
from hashlib import sha256
from typing import Dict


class ServerMsgs:
    db = DBHandler()

    @classmethod
    def send_msg(cls, request_data: Dict[str, str]) -> GenericResponse:
        request = SendMsg(**request_data)
        hashed_password = sha256(bytes(request.sender_password, 'utf-8')).hexdigest()
        if not CookieHandler.verify(request.sender_email + hashed_password, request.cookie):
            response_data = {'status': False, 'message': 'you are unauthorized'}
            return GenericResponse(**response_data)
        sender = cls.db.query('users', {'email': request.sender_email})
        receiver = cls.db.query('users', {'email': request.receiver_email})
        if receiver:
            cls.db.write('msgs', {'sender_uid': sender[0][0], 'receiver_uid': receiver[0][0], 'subject': request.subject,
                                  'message': request.msg})
            response_data = {'status': True, 'message': 'sent message'}
            return GenericResponse(**response_data)
        response_data = {'status': False, 'message': 'receiver email does not exist'}
        return GenericResponse(**response_data)

    @classmethod
    def get_msgs(cls, request_data: Dict[str, str]) -> GenericResponse:
        request = GetMsg(**request_data)
        hashed_password = sha256(bytes(request.sender_password, 'utf-8')).hexdigest()
        if not cls.db.query('users', {'email': request.sender_email}):
            cls.db.write('users', {'email': request.email, 'password': hashed_password, 'name': request.name})
            response_data = {'status': True, 'message': 'successfully signed up'}
            response = GenericResponse(**response_data)
        else:
            response_data = {'status': True, 'message': 'username already exists'}
            response = GenericResponse(**response_data)
        return response
