import pymysql
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def db_con():
    return pymysql.connect(
        host="DBHost",
        database="DBName",
        user="DBUser",
        password="DBPassword",
    )
