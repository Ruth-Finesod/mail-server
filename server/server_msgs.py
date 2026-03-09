import base64
from collections import defaultdict
from typing import List, Any, Dict

from DBHandler import DBHandler
from communication_objects import SendMsg, GetMsg, GenericResponse, MsgResponse, ReadMsg, Attachment


class ServerMsgs:
    db = DBHandler()
    USERS_TABLE = 'users'
    MSGS_TABLE = 'msgs'
    ATTACHMENTS_TABLE = 'attachments'
    ATTACHMENTS_DIR = './attachments'

    @classmethod
    def send_msg(cls, request: SendMsg) -> GenericResponse:
        """
        adds a message given in the request_data to the db
        :param request: SendMsg
        :return: in the format of GenericResponse, returns the status of the action
        """
        sender = cls.db.query(cls.USERS_TABLE, {'email': request.email})[0]
        receiver = cls.db.query(cls.USERS_TABLE, {'email': request.receiver_email})
        if receiver:
            receiver = receiver[0]
            message_data = {'sender_uid': sender[0], 'receiver_uid': receiver[0], 'subject': request.subject,
                            'message': request.msg, 'read': False}
            if request.reply_to:
                replied_to = cls.db.query(cls.MSGS_TABLE, {'uid': request.reply_to})[0]
                message_data['conv_uid'] = replied_to[5]
            else:
                message_data['conv_uid'] = cls.db.get_max('conv_uid', cls.MSGS_TABLE)
            msg_uid = cls.db.write(cls.MSGS_TABLE, message_data)
            cls.send_attachments(msg_uid, request.attachments)
            response_data = {'status': True, 'message': 'sent message'}
        else:
            response_data = {'status': False, 'message': 'receiver email does not exist'}
        return GenericResponse(**response_data)

    @classmethod
    def get_msgs(cls, request: GetMsg) -> List[List[MsgResponse]]:
        """
        fetches all the messages to a specific user
        :param request: GetMsg with the information of the requested user
        :return: List of Lists of MsgResponses with the email information divided by conv uid
        """
        receiver = cls.db.query(cls.USERS_TABLE, {'email': request.email})[0]
        messages_query = {'receiver_uid': receiver[0]}
        if not request.read:
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
            attachment = Attachment(**attachment)
            uid = cls.db.get_max('uid', cls.ATTACHMENTS_TABLE)
            file_data = base64.b64decode(attachment.file_data)
            with open(cls.ATTACHMENTS_TABLE + '\\' + str(uid), 'wb') as f:
                f.write(file_data)
            db_attachment = {'uid': uid, 'file_name': attachment.file_name, 'msg_uid': msg_uid}
            cls.db.write(cls.ATTACHMENTS_TABLE, db_attachment)

    @classmethod
    def get_attachments(cls, msg_uid) -> List[Attachment]:
        attachments = cls.db.query(cls.ATTACHMENTS_TABLE, {'msg_uid': msg_uid})
        organized_atts = []
        for attachment in attachments:
            with open(cls.ATTACHMENTS_TABLE + '\\' + str(attachment[0]), 'rb') as f:
                file_data = f.read()
            organized_att = {'file_name': attachment[1], 'file_data': base64.b64encode(file_data).decode()}
            organized_atts.append(Attachment(**organized_att))
        return organized_atts

    @classmethod
    def read_msg(cls, request: ReadMsg) -> GenericResponse:
        """
        adds a message given in the request_data to the db
        :param request: dict of strings in the format of ReadMsg (only includes the msg uid)
        :return: in the format of GenericResponse, returns the status of the action
        """
        cls.db.update(cls.MSGS_TABLE, {'uid': request.uid}, {'read': True})
        response_data = {'status': True, 'message': 'message was read'}
        return GenericResponse(**response_data)
