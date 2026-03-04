from client.msg_handler import MsgHandler
from client_auth import ClientAuth


def main():
    user = ClientAuth()
    while True:
        MsgHandler(user)

if __name__ == '__main__':
    main()
