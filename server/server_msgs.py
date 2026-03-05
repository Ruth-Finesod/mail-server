from hashlib import sha256
from typing import Dict
from typing import List

from DBHandler import DBHandler
from communication_objects import SendMsg, GetMsg, GenericResponse, MsgResponse
from cookie_handler import CookieHandler


class ServerMsgs:
    db = DBHandler()

    @classmethod
    def send_msg(cls, request_data: Dict[str, str]) -> GenericResponse:
        request = SendMsg(**request_data)
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        if not CookieHandler.verify(request.email + hashed_password, request.cookie):
            response_data = {'status': False, 'message': 'you are unauthorized'}
            return GenericResponse(**response_data)
        sender = cls.db.query('users', {'email': request.email})
        receiver = cls.db.query('users', {'email': request.receiver_email})
        if receiver:
            cls.db.write('msgs',
                         {'sender_uid': sender[0][0], 'receiver_uid': receiver[0][0], 'subject': request.subject,
                          'message': request.msg})
            response_data = {'status': True, 'message': 'sent message'}
            return GenericResponse(**response_data)
        response_data = {'status': False, 'message': 'receiver email does not exist'}
        return GenericResponse(**response_data)

    @classmethod
    def get_msgs(cls, request_data: Dict[str, str]) -> List[MsgResponse]:
        request = GetMsg(**request_data)
        hashed_password = sha256(bytes(request.password, 'utf-8')).hexdigest()
        if not CookieHandler.verify(request.email + hashed_password, request.cookie):
            return []
        receiver = cls.db.query('users', {'email': request.email})
        messages = cls.db.query('msgs', {'receiver_uid': receiver[0][0]})
        all_messages_data = []
        for message in messages:
            sender = cls.db.query('users', {'uid': message[1]})
            request_data = {'sender_email': sender[0][1], 'subject': message[3], 'msg': message[4]}
            message_data = MsgResponse(**request_data)
            all_messages_data.append(message_data)
        return all_messages_data
