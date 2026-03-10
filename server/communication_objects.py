from pydantic import BaseModel
from typing import List, Dict, Any


class SignUp(BaseModel):
    email: str
    password: str
    full_name: str


class Login(BaseModel):
    email: str
    password: str


class Attachment(BaseModel):
    file_name: str
    file_data: str


class SendMsg(BaseModel):
    email: str
    password: str
    cookie: str
    receiver_email: str
    subject: str
    msg: str
    reply_to: int
    attachments: List[Dict[str, Any]]


class GetMsg(BaseModel):
    email: str
    password: str
    cookie: str
    read: bool


class MsgResponse(BaseModel):
    uid: int
    sender_email: str
    subject: str
    msg: str
    attachments: List[Dict[str, Any]]


class ReadMsg(BaseModel):
    uid: int
