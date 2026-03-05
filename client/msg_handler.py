from base_client_class import BaseClass
from client.client_auth import ClientAuth
from client_send import send
from communication_objects import SendMsg, GenericResponse, GetMsg, MsgResponse, ReadMsg
from server_methods import ServerMethods


class MsgHandler(BaseClass):
    CHOICES = {
        'q': 'quit_app',
        's': 'send_message',
        'r': 'receive_messages',
    }

    def __init__(self, user: ClientAuth):
        self.user = user
        self.pick_method()

    @property
    def _user_parms(self):
        return {'email': self.user.email, 'password': self.user.password, 'cookie': self.user.cookie}

    def send_message(self, reply_to=0):
        """
        send message to the server in SendMsg format
        receive response as GenericResponse and print
        """
        receiver = input("send message to: ")
        subject = input("subject of the message: ")
        message = input("message: ")
        msg = {'receiver_email': receiver, 'subject': subject, 'msg': message, 'reply_to': reply_to}
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
        new_or_all = input('n: receive only new messages\n a: receive all messages')
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
                self.read_msg(response[int(msg_num) - 1])

    def print_msg(self, msg):
        send({ServerMethods.READ_MSG.value: ReadMsg(uid=msg.uid).model_dump()})
        print(f'from: {msg.sender_email}')
        print(f'subject: {msg.subject}')
        print(f'message: {msg.msg}\n')

    def read_msg(self, msg):
        if len(msg) == 1:
            msg = MsgResponse(**msg[0])
            self.print_msg(msg)
            next_method = input('q: to return to messages manu\nr: to reply to message\n ')
            if next_method == 'q':
                return
            if next_method == 'r':
                print(f'replying to {msg.sender_email}')
                self.send_message(reply_to=msg.uid)
        else:
            for i, inner_msg in enumerate(msg):
                inner_msg = MsgResponse(**inner_msg)
                print(f'{i + 1}')
                self.print_msg(inner_msg)
            next_method = input('q: to return to messages manu\nr: to reply to message\n ')
            if next_method == 'q':
                return
            if next_method == 'r':
                msg_num = int(input("enter number of the message to reply to: "))
                self.send_message(reply_to=msg[msg_num - 1].uid)

    @staticmethod
    def quit_app():
        quit()
