from pydantic import BaseModel


class SignUp(BaseModel):
    email: str
    password: str
    full_name: str


class Login(BaseModel):
    email: str
    password: str


class SendMsg(BaseModel):
    email: str
    password: str
    cookie: str
    receiver_email: str
    subject: str
    msg: str
    reply_to: int


class GetMsg(BaseModel):
    email: str
    password: str
    cookie: str
    read: bool


class GenericResponse(BaseModel):
    status: bool
    message: str


class LogInResponse(BaseModel):
    status: bool
    message: str
    cookie: str


class MsgResponse(BaseModel):
    uid: int
    sender_email: str
    subject: str
    msg: str


class ReadMsg(BaseModel):
    uid: int
