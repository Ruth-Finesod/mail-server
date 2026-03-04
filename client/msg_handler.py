from client.client_auth import ClientAuth
from communication_objects import SendMsg, LogInResponse
from server_methods import ServerMethods
from client_send import send


class MsgHandler:
    def __init__(self, user: ClientAuth, method: ServerMethods):
        self.user = user
        if method == ServerMethods.SEND_MESSAGE:
            self.send_message()
        if method == ServerMethods.RECEIVE_MESSAGES:
            self.receive_message()

    def send_message(self):
        receiver = input("send message to: ")
        subject = input("subject of the message: ")
        message = input("message: ")
        msg = {'sender_email': self.user.email, 'sender_password': self.user.password, 'cookie': self.user.cookie,
                      'receiver_email': receiver, 'subject': subject, 'msg': message}
        body_request = SendMsg(**msg)
        request = {ServerMethods.SEND_MESSAGE.value: body_request.model_dump()}
        response = send(request)
        response = LogInResponse(**response)
        print(response.message)

def receive_message(self):
    pass



