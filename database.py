import os
from dotenv import load_dotenv
import mysql.connector as mysql

def connect_db():
    return mysql.connect(
        user=os.environ.get('DB_USER'),
        host=os.environ.get('DB_HOST'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_DATABASE'),
    )