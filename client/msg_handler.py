import os.path
from tkinter import filedialog, Tk
from subprocess import Popen
import pathlib

from base_client_class import BaseClass
from client.client_auth import ClientAuth
from client_send import send
from communication_objects import SendMsg, GenericResponse, GetMsg, MsgResponse, ReadMsg, Attachment
from server_methods import ServerMethods
import base64


class MsgHandler(BaseClass):
    MAIN_CHOICES = {
        'q': 'quit_app',
        's': 'send_message',
        'r': 'receive_messages',
    }

    def __init__(self, user: ClientAuth):
        self.user = user
        self.pick_method(self.MAIN_CHOICES)

    @property
    def _user_parms(self):
        return {'email': self.user.email, 'password': self.user.password, 'cookie': self.user.cookie}

    def send_message(self, reply_to=0, receiver='', subject=''):
        """
        send message to the server in SendMsg format
        receive response as GenericResponse and print
        """
        if reply_to == 0:
            receiver = input("send message to: ")
            subject = input("subject of the message: ")
        message = input("message: ")
        attachment = input("do you want to attach files? (y/n): ")
        while attachment not in ('y', 'n'):
            attachment = input("do you want to attach files? (y/n): ")
        attachments = self.attach_file() if attachment == 'y' else []
        msg = {'receiver_email': receiver, 'subject': subject, 'msg': message, 'reply_to': reply_to,
               'attachments': attachments}
        body_request = SendMsg(**self._user_parms, **msg)
        request = {ServerMethods.SEND_MESSAGE.value: body_request.model_dump()}
        response = send(request)
        response = GenericResponse(**response)
        print(response.message)

    def receive_messages(self):
        """
        request to receive messages from server in GetMsg format
        receive list of messages as MsgResponse object and print
        """
        receive_options = {'n': False, 'a': True}
        new_or_all = input('n: receive only new messages\na: receive all messages\nyour choice: ')
        while new_or_all not in receive_options:
            new_or_all = input('you must choose from the options above: ')
        body_request = GetMsg(**self._user_parms, read=receive_options[new_or_all])
        request = {ServerMethods.RECEIVE_MESSAGES.value: body_request.model_dump()}
        response = send(request)
        print('\n')
        for i, msg in enumerate(response):
            if msg:
                msg = MsgResponse(**msg[0])
                print(f'{i + 1}. from: {msg.sender_email} | subject: {msg.subject}')
            else:
                print('no messages\n')
                return
        while True:
            msg_num = input("q: to return to main\nenter number of the message to read: ")
            if msg_num == 'q':
                return
            else:
                while not (msg_num.isalnum() and 1 <= int(msg_num) <= len(response)):
                    msg_num = input('you must choose from the messages above: ')
                self.read_msg(response[int(msg_num) - 1])

    def read_msg(self, msgs):
        msgs = msgs if type(msgs) is list else [msgs]
        for msg in msgs:
            msg = MsgResponse(**msg)
            send({ServerMethods.READ_MSG.value: ReadMsg(uid=msg.uid).model_dump()})
            print(f'from: {msg.sender_email}')
            print(f'subject: {msg.subject}')
            print(f'message: {msg.msg}\n')
            if msg.attachments:
                print('attachments: ')
                attachments = [Attachment(**attachment) for attachment in msg.attachments]
                for attachment in attachments:
                    print(attachment.file_name)
                download = input('do you want to download attachment? (y/n): ')
                while download not in ('y', 'n'):
                    download = input("do you want to attach files? (y/n): ")
                if download == 'y':
                    self.download_attachments(attachments)
        next_method = input('q: to return to messages manu\nr: to reply to message\nyour choice: ')
        while next_method not in ('q', 'r'):
            next_method = input('you must choose from the options above: ')
        if next_method == 'q':
            return
        if next_method == 'r':
            self.send_message(reply_to=msg.uid, receiver=msg.sender_email, subject=msg.subject)

    @staticmethod
    def attach_file():
        attachments = []
        Tk().withdraw()
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            file_name = os.path.basename(file_path)
            attachments.append({'file_name': file_name, 'file_data': base64.b64encode(file_data).decode()})
        return attachments

    @staticmethod
    def download_attachments(attachments):
        for attachment in attachments:
            file_data = base64.b64decode(attachment.file_data)
            new_file_path = pathlib.Path.home() / 'Downloads' / attachment.file_name
            with open(new_file_path, 'wb') as f:
                f.write(file_data)
                Popen(f'explorer {new_file_path}')

    @staticmethod
    def quit_app():
        quit()
