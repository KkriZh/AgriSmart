import mysql.connector
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as err:
        print("MySQL connection error:", err)
        return None
