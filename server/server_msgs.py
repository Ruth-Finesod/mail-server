from collections import defaultdict
from typing import List, Any, Dict, Tuple

from DBHandler import DBHandler
from communication_objects import SendMsg, GetMsg, GenericResponse, MsgResponse, ReadMsg, Attachment
from cookie_handler import CookieHandler


class ServerMsgs:
    db = DBHandler()
    USERS_TABLE = 'users'
    MSGS_TABLE = 'msgs'
    ATTACHMENTS_TABLE = 'attachments'

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
        sender = cls.db.query(cls.USERS_TABLE, {'email': request.email})[0]
        receiver = cls.db.query(cls.USERS_TABLE, {'email': request.receiver_email})[0]
        if receiver:
            message_data = {'sender_uid': sender[0], 'receiver_uid': receiver[0], 'subject': request.subject,
                            'message': request.msg, 'read': False}
            if request.reply_to:
                replied_to = cls.db.query(cls.MSGS_TABLE, {'uid': request.reply_to})[0]
                message_data['conv_uid'] = replied_to[5]
            else:
                message_data['conv_uid'] = cls.db.get_max('conv_uid', cls.USERS_TABLE)
            msg_uid = cls.db.write(cls.MSGS_TABLE, message_data)
            cls.send_attachments(msg_uid, request.attachments)
            response_data = {'status': True, 'message': 'sent message'}
        else:
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
        receiver = cls.db.query(cls.USERS_TABLE, {'email': request.email})[0]
        messages_query = {'receiver_uid': receiver[0]}
        if request.read is False:
            messages_query['read'] = request.read
        messages = cls.db.query(cls.MSGS_TABLE, messages_query)
        conv_uids = defaultdict(list)
        for message in messages:
            sender = cls.db.query(cls.USERS_TABLE, {'uid': message[1]})[0]
            attachments = [attach.model_dump() for attach in cls.get_attachments(message[0])]
            request_data = {'uid': message[0], 'sender_email': sender[1], 'subject': message[3], 'msg': message[4],
                            'attachments': attachments}
            message_data = MsgResponse(**request_data)
            conv_uids[message[5]].append(message_data)
        return list(conv_uids.values())

    @classmethod
    def send_attachments(cls, msg_uid: int, attachments: List[Dict[str, Any]]):
        for attachment in attachments:
            attachment = Attachment(**attachment).model_dump()
            attachment['msg_uid'] = msg_uid
            cls.db.write(cls.ATTACHMENTS_TABLE, attachment)

    @classmethod
    def get_attachments(cls, msg_uid) -> List[Attachment]:
        attachments = cls.db.query(cls.ATTACHMENTS_TABLE, {'msg_uid': msg_uid})
        organized_atts = []
        for attachment in attachments:
            organized_att = {'file_name': attachment[1], 'file_data': attachments[2]}
            organized_atts.append(Attachment(**organized_att))
        return organized_atts

    @classmethod
    def read_msg(cls, request_data: Dict[str, str]) -> GenericResponse:
        """
        adds a message given in the request_data to the db
        :param request_data: dict of strings in the format of ReadMsg (only includes the msg uid)
        :return: in the format of GenericResponse, returns the status of the action
        """
        request = ReadMsg(**request_data)
        cls.db.update(cls.MSGS_TABLE, {'uid': request.uid}, {'read': True})
        response_data = {'status': True, 'message': 'message was read'}
        return GenericResponse(**response_data)
