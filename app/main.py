from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.chat import chat
import uuid

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return open("templates/chat.html", encoding="utf-8").read()

@app.post("/chat")
async def chat_api(req: Request):
    data = await req.json()
    session_id = data.get("session_id") or str(uuid.uuid4())
    reply = chat(session_id, data["message"])
    return JSONResponse({"reply": reply, "session_id": session_id})
