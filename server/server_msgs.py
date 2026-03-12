import base64
from collections import defaultdict
from typing import List, Any, Dict

from DBHandler import DBHandler
from communication_objects import SendMsg, GetMsg, MsgResponse, ReadMsg, Attachment
from errors import *


class DBMessage:
    def __init__(self, row):
        self.uid, self.sender_uid, self.subject, self.message, self.read, self.conv_uid, self.receivers_uid = row
        self.receivers_uid = [int(receiver_uid) for receiver_uid in self.receivers_uid.split(',')]
        self.read = [int(read) for read in str(self.read).split(',')]


class ServerMsgs:
    db = DBHandler()
    USERS_TABLE = 'users'
    MSGS_TABLE = 'msgs'
    ATTACHMENTS_TABLE = 'attachments'
    ATTACHMENTS_DIR = './attachments'

    @classmethod
    def send_msg(cls, request: SendMsg) -> str:
        """
        adds a message given in the request_data to the db
        :param request: SendMsg
        :return: message string or errors
        """
        sender = cls.db.query(cls.USERS_TABLE, {'email': request.email})[0]
        receivers = []
        msg = ''
        receivers_exist = True
        for receiver_email in request.receivers_email:
            receiver = cls.db.query(cls.USERS_TABLE, {'email': receiver_email})
            if not receiver:
                msg += f'{receiver_email}, '
                receivers_exist = False
            else:
                receivers.append(receiver[0])
        if not receivers_exist:
            raise BadRequestError(msg + 'does not exists')
        message_data = {'sender_uid': sender[0], 'receivers_uid': ','.join(map(str, [receiver[0] for receiver in receivers])),
                        'subject': request.subject, 'message': request.msg, 'read': ','.join(map(str, [0 for receiver in receivers]))}
        if request.reply_to:
            replied_to = DBMessage(cls.db.query(cls.MSGS_TABLE, {'uid': request.reply_to})[0])
            message_data['conv_uid'] = replied_to.conv_uid
        else:
            message_data['conv_uid'] = cls.db.get_max('conv_uid', cls.MSGS_TABLE)
        msg_uid = cls.db.write(cls.MSGS_TABLE, message_data)
        cls.send_attachments(msg_uid, request.attachments)
        return 'sent message'

    @classmethod
    def get_msgs(cls, request: GetMsg) -> List[List[MsgResponse]]:
        """
        fetches all the messages to a specific user
        :param request: GetMsg with the information of the requested user
        :return: List of Lists of MsgResponses with the email information divided by conv uid
        """
        user = cls.db.query(cls.USERS_TABLE, {'email': request.email})[0]
        messages = cls.db.query_in(cls.MSGS_TABLE, {'receivers_uid': user[0]})
        messages += cls.db.query(cls.MSGS_TABLE, {'sender_uid': user[0]})
        conv_uids = defaultdict(list)
        for message in messages:
            message = DBMessage(message)
            receivers = [cls.db.query(cls.USERS_TABLE, {'uid': receiver_uid})[0] for receiver_uid in message.receivers_uid]
            sender = cls.db.query(cls.USERS_TABLE, {'uid': message.sender_uid})[0]
            attachments = cls.get_attachments(message.uid)
            if sender == user:
                read = 1
            else:
                read = message.read[message.receivers_uid.index(user[0])]
            request_data = {'uid': message.uid, 'sender_email': sender[1],
                            'receivers_email': [receiver[1] for receiver in receivers], 'subject': message.subject,
                            'msg': message.message, 'attachments': attachments, 'read': read}
            message_data = MsgResponse(**request_data)
            conv_uids[message.conv_uid].append(message_data)
        return list(conv_uids.values())

    @classmethod
    def send_attachments(cls, msg_uid: int, attachments: List[Attachment]):
        for attachment in attachments:
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
    def read_msg(cls, request: ReadMsg) -> str:
        """
        adds a message given in the request_data to the db
        :param request: dict of strings in the format of ReadMsg (only includes the msg uid)
        :return: message string or errors
        """
        msg = DBMessage(cls.db.query(cls.MSGS_TABLE, {'uid': request.uid})[0])
        user = cls.db.query(cls.USERS_TABLE, {'email': request.email})[0]
        user_uid = user[0]
        msg.read[msg.receivers_uid.index(user_uid)] = 1
        cls.db.update(cls.MSGS_TABLE, {'uid': request.uid}, {'read': ','.join(map(str, [str(read) for read in msg.read]))})
        return 'message was read'
