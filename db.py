import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def test_connection():
    conn = get_connection()
    print("Database connected successfully")
    conn.close()

def save_chat_log(session_id, user_message, ai_message):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chat_logs (session_id, user_message, ai_message)
        VALUES (%s, %s, %s)
        """,
        (session_id, user_message, ai_message)
    )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_connection()