from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import resend

resend.api_key = os.environ["KEYRENSED"]

def aviso(user):
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": [f"{user}"],
        "subject": "Alguien esta en la puerta por favor revisa la camara",
        "html": "<strong>Alerta!</strong>",
    }

    email = resend.Emails.send(params)

app = FastAPI()
user=[]

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    with open("static/registro.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.put("/{email}")
async def update_item(email: str):
    user.append(email)
    print(user)
    return True

@app.get("/lobby")
async def get():
    with open("static/lobby.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data!="c":
            await websocket.send_text(f"Message text was: {data}")
        else:
            for email in user:
                aviso(email)
