from base_client_class import BaseClass
from client.client_auth import ClientAuth
from client_send import send
from communication_objects import SendMsg, GenericResponse, GetMsg, MsgResponse
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

    def send_message(self):
        """
        send message to the server in SendMsg format
        receive response as GenericResponse and print
        """
        receiver = input("send message to: ")
        subject = input("subject of the message: ")
        message = input("message: ")
        msg = {'receiver_email': receiver, 'subject': subject, 'msg': message}
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
        body_request = GetMsg(**self._user_parms)
        request = {ServerMethods.RECEIVE_MESSAGES.value: body_request.model_dump()}
        response = send(request)
        print('\n')
        if response:
            for msg in response:
                msg = MsgResponse(**msg)
                print('new message')
                print(f'from: {msg.sender_email}')
                print(f'subject: {msg.subject}')
                print(f'message: {msg.msg}\n')
        else:
            print('no messages\n')

    @staticmethod
    def quit_app():
        quit()