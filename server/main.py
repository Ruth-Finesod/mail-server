from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from communication_objects import *
from errors import *
from server_auth import ServerAuth
from server_msgs import ServerMsgs

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})


@app.get("/log_in", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/log_in.html", {"request": request})


@app.get("/sign_up", response_class=HTMLResponse)
def sign_up_page(request: Request):
    return templates.TemplateResponse("auth/sign_up.html", {"request": request})


@app.get("/mails", response_class=HTMLResponse)
def sign_up_page(request: Request):
    return templates.TemplateResponse("mails/main.html", {"request": request})


@app.get("/sign_up", response_class=HTMLResponse)
def sign_up_page(request: Request):
    return templates.TemplateResponse("dir/sign_up.html", {"request": request})

@app.exception_handler(BadRequestError)
async def auth_exception_handler(request: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )


@app.post("/auth/login")
def log_in(request: Login) -> Dict[str, str]:
    return {"message": ServerAuth.log_in(request)}


@app.post("/auth/signup")
def sign_up(request: SignUp) -> Dict[str, str]:
    return {"message": ServerAuth.sign_up(request)}


@app.post("/msgs/send")
def send_msg(request: SendMsg):
    return {"message": ServerMsgs.send_msg(request)}


@app.post("/msgs/receive")
def receive_msgs(request: GetMsg) -> List[List[MsgResponse]]:
    return ServerMsgs.get_msgs(request)


@app.post("/msgs/read")
def read_msg(request: ReadMsg) -> str:
    return ServerMsgs.read_msg(request)
