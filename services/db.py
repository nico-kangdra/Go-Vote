import pymysql
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def db_con():
    return pymysql.connect(
        host="DB_HOST",
        database="DB_NAME",
        user="DB_USER",
        password="DB_PASS",
    )
