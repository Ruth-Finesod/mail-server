from pydantic import BaseModel


class SignUp(BaseModel):
    email: str
    password: str
    name: str


class Login(BaseModel):
    email: str
    password: str


class SendMsg(BaseModel):
    sender_email: str
    sender_password: str
    cookie: str
    receiver_email: str
    subject: str
    msg: str


class GetMsg(BaseModel):
    email: str
    password: str
    cookie: str


class GenericResponse(BaseModel):
    status: bool
    message: str


class LogInResponse(BaseModel):
    status: bool
    message: str
    cookie: str


class MsgResponse(BaseModel):
    sender_email: str
    sent_time: float
    subject: str
    msg: str
