import sqlite3

DB_PATH = "chatbot.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn
