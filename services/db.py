import pymysql


def db_con():
    return pymysql.connect(host="localhost", db="govote", user="root", password="root")
