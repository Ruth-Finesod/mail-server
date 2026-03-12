from pydantic import BaseModel
from typing import List, Dict, Any, Optional


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
    receivers_email: List[str]
    subject: str
    msg: str
    reply_to: int
    attachments: List[Attachment]


class GetMsg(BaseModel):
    email: str


class MsgResponse(BaseModel):
    uid: int
    sender_email: str
    receivers_email: List[str]
    subject: str
    msg: str
    attachments: List[Attachment]
    read: bool


class ReadMsg(BaseModel):
    uid: int
    email: str
