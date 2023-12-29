import pymysql
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def db_con():
    return pymysql.connect(
        host="34.101.42.68",
        db="govote",
        user="govote",
        password="123",
    )
