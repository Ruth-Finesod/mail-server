from enum import Enum


class ServerMethods(Enum):
    LOG_IN = 1
    SIGN_UP = 2
    SEND_MESSAGE = 3
    RECEIVE_MESSAGES = 4
    READ_MSG = 5
