import pymysql
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def db_con():
    return pymysql.connect(
        host=getenv("DB_HOST"),
        db=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASS"),
    )