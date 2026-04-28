import psycopg2
from config import load_config

def get_connection():
    try:
        conn = psycopg2.connect(**load_config())
        print("Connected successfully")
        return conn
    except Exception as e:
        print("Connection error:", e)
        return None


conn = get_connection()
if conn:
    conn.close()