import pymysql
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def db_con():
    return pymysql.connect(
        host="localhost",
        database="govote",
        user="user",
        password="@a(*9KQLz/M(b)gC",
    )
