from typing import Dict
from typing import List

from DBHandler import DBHandler
from communication_objects import SendMsg, GetMsg, GenericResponse, MsgResponse, ReadMsg
from cookie_handler import CookieHandler
from collections import defaultdict


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
            message_data = {'sender_uid': sender[0][0], 'receiver_uid': receiver[0][0], 'subject': request.subject,
                            'message': request.msg}
            if request.reply_to:
                replied_to = cls.db.query(cls.USERS_TABLE, {'uid': request.reply_to})[0]
                message_data['conv_uid'] = replied_to[5]
            else:
                message_data['conv_uid'] = cls.db.get_max('conv_uid', cls.USERS_TABLE)
            cls.db.write(cls.MSGS_TABLE, message_data)
            response_data = {'status': True, 'message': 'sent message'}
            return GenericResponse(**response_data)
        response_data = {'status': False, 'message': 'receiver email does not exist'}
        return GenericResponse(**response_data)

    @classmethod
    def get_msgs(cls, request_data: Dict[str, str]) -> List[List[MsgResponse]]:
        """
        fetches all the messages to a specific user
        :param request_data: dict of strings in format of GetMsg with the information of the requested user
        :return: List of Lists of MsgResponses with the email information divided by conv uid
        """
        request = GetMsg(**request_data)
        if not CookieHandler.verify(request.email + request.password, request.cookie):
            return []
        receiver = cls.db.query(cls.USERS_TABLE, {'email': request.email, 'read': request.read})
        messages = cls.db.query(cls.MSGS_TABLE, {'receiver_uid': receiver[0][0]})
        conv_uids = defaultdict(list)
        for message in messages:
            sender = cls.db.query(cls.USERS_TABLE, {'uid': message[1]})
            request_data = {'uid': message[0], 'sender_email': sender[0][1], 'subject': message[3], 'msg': message[4]}
            message_data = MsgResponse(**request_data)
            conv_uids[message[5]].append(message_data)
        return list(conv_uids.values())

    @classmethod
    def read_msg(cls, request_data: Dict[str, str]) -> GenericResponse:
        """
        adds a message given in the request_data to the db
        :param request_data: dict of strings in the format of ReadMsg (only includes the msg uid)
        :return: in the format of GenericResponse, returns the status of the action
        """
        request = ReadMsg(**request_data)
        if not CookieHandler.verify(request.email + request.password, request.cookie):
            response_data = {'status': False, 'message': 'you are unauthorized'}
            return GenericResponse(**response_data)
        cls.db.update(cls.MSGS_TABLE, {'uid': request.uid}, {'read': True})
        response_data = {'status': True, 'message': 'message was read'}
        return GenericResponse(**response_data)
