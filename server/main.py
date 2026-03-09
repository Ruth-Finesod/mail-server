from fastapi import FastAPI

from communication_objects import *
from server_auth import ServerAuth
from server_msgs import ServerMsgs

app = FastAPI()


@app.post("/auth/login")
def log_in(request: Login) -> LogInResponse:
    return ServerAuth.log_in(request)


@app.post("/auth/signup")
def sign_up(request: SignUp) -> GenericResponse:
    return ServerAuth.sign_up(request)


@app.post("/msgs/send")
def send_msg(request: SendMsg):
    return ServerMsgs.send_msg(request)


@app.post("/msgs/receive")
def receive_msgs(request: GetMsg) -> List[List[MsgResponse]]:
    return ServerMsgs.get_msgs(request)


@app.post("/msgs/receive")
def read_msg(request: ReadMsg) -> GenericResponse:
    return ServerMsgs.read_msg(request)
