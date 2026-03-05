from client.msg_handler import MsgHandler
from client_auth import ClientAuth


def main():
    """
    make authentication object and then always run MsgHandler
    """
    user = ClientAuth()
    while True:
        MsgHandler(user)


if __name__ == '__main__':
    main()
