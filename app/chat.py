import google.generativeai as genai
from app.rag import retrieve
from app.prompt import SYSTEM_PROMPT
from app.db import get_db
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_history(session_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT role, message FROM chat_history WHERE session_id=?", (session_id,))
    rows = cur.fetchall()
    return "\n".join([f"{r}: {m}" for r, m in rows])

def save_message(session_id, role, message):
    db = get_db()
    cur = db.cursor()
    cur.execute(
    "SELECT role, message FROM chat_history WHERE session_id=?",
    (session_id,)
)

    db.commit()

def chat(session_id, user_input):
    docs = retrieve(user_input)
    history = get_history(session_id)

    prompt = f"""
{SYSTEM_PROMPT}

Lịch sử:
{history}

Dữ liệu laptop:
{chr(10).join(docs)}

Khách hàng hỏi:
{user_input}
"""
    response = model.generate_content(prompt).text

    save_message(session_id, "user", user_input)
    save_message(session_id, "assistant", response)

    return response
