from client.client_auth import ClientAuth
from communication_objects import SendMsg, GenericResponse, GetMsg, MsgResponse
from server_methods import ServerMethods
from client_send import send


class MsgHandler:
    def __init__(self, user: ClientAuth):
        self.user = user
        self.pick_method()


    def send_message(self):
        receiver = input("send message to: ")
        subject = input("subject of the message: ")
        message = input("message: ")
        msg = {'sender_email': self.user.email, 'sender_password': self.user.password, 'cookie': self.user.cookie,
                      'receiver_email': receiver, 'subject': subject, 'msg': message}
        body_request = SendMsg(**msg)
        request = {ServerMethods.SEND_MESSAGE.value: body_request.model_dump()}
        response = send(request)
        response = GenericResponse(**response)
        print(response.message)

    def receive_message(self):
        body_request = GetMsg(email=self.user.email, password=self.user.password, cookie=self.user.cookie)
        request = {ServerMethods.RECEIVE_MESSAGES.value: body_request.model_dump()}
        response = send(request)
        for msg in response:
            msg = MsgResponse(**msg)
            print('new message')
            print(f'from: {msg.sender_email}')
            print(f'subject: {msg.subject}')
            print(f'message: {msg.msg}\n')

    def pick_method(self):
        print('what do you like to you do?')
        choices = {'s': self.send_message, 'r': self.receive_message}
        choice = input('s: send message\nr: receive messages\nyour choice: ')
        picked_method = choices.get(choice)
        if picked_method:
            picked_method()
        else:
            print('you must pick one of the presented options')
            self.pick_method()


