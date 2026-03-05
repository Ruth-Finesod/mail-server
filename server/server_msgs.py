from typing import Dict
from typing import List

from DBHandler import DBHandler
from communication_objects import SendMsg, GetMsg, GenericResponse, MsgResponse
from cookie_handler import CookieHandler


class ServerMsgs:
    db = DBHandler()
    USERS_TABLE = 'users'
    MSGS_TABLE = 'msgs'

    @classmethod
    def send_msg(cls, request_data: Dict[str, str]) -> GenericResponse:
        """
        adds a message given in the request_data to the db
        :param request_data: dict of strings in the format of SendMsg
        :return: in the format of GenericResponse, returns the status of the action
        """
        request = SendMsg(**request_data)
        if not CookieHandler.verify(request.email + request.password, request.cookie):
            response_data = {'status': False, 'message': 'you are unauthorized'}
            return GenericResponse(**response_data)
        sender = cls.db.query(cls.USERS_TABLE, {'email': request.email})
        receiver = cls.db.query(cls.USERS_TABLE, {'email': request.receiver_email})
        if receiver:
            cls.db.write(cls.MSGS_TABLE,
                         {'sender_uid': sender[0][0], 'receiver_uid': receiver[0][0], 'subject': request.subject,
                          'message': request.msg})
            response_data = {'status': True, 'message': 'sent message'}
            return GenericResponse(**response_data)
        response_data = {'status': False, 'message': 'receiver email does not exist'}
        return GenericResponse(**response_data)

    @classmethod
    def get_msgs(cls, request_data: Dict[str, str]) -> List[MsgResponse]:
        """
        fetches all the messages to a specific user
        :param request_data: dict of strings in format of GetMsg with the information of the requested user
        :return: List of MsgResponses with the email information
        """
        request = GetMsg(**request_data)
        if not CookieHandler.verify(request.email + request.password, request.cookie):
            return []
        receiver = cls.db.query(cls.USERS_TABLE, {'email': request.email})
        messages = cls.db.query(cls.MSGS_TABLE, {'receiver_uid': receiver[0][0]})
        all_messages_data = []
        for message in messages:
            sender = cls.db.query(cls.USERS_TABLE, {'uid': message[1]})
            request_data = {'sender_email': sender[0][1], 'subject': message[3], 'msg': message[4]}
            message_data = MsgResponse(**request_data)
            all_messages_data.append(message_data)
        return all_messages_data
