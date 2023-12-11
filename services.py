from db import db_con
from hashlib import sha256

def hash(txt):
    return sha256(txt.encode('utf-8')).hexdigest()

def execute(sql):
    conn = db_con()
    curs = conn.cursor()
    curs.execute(sql)
    return {"con":conn, "cur":curs}


def close(item):
    for x in item:
        x.close()


def get_nik(nik):
    item = execute(f"SELECT * FROM users WHERE nik = {nik}")
    res = item["cur"].fetchone()
    close(item)
    return res


def get_count():
    item1 = execute(f"SELECT COUNT(*) FROM users WHERE vote = 1")
    item2 = execute(f"SELECT COUNT(*) FROM users WHERE vote = 2")
    item3 = execute(f"SELECT COUNT(*) FROM users WHERE vote = 3")
    res = [item1["cur"].fetchone()[0], item2["cur"].fetchone()[0], item3["cur"].fetchone()[0]]
    close(item1)
    close(item2)
    close(item3)
    return res


def set_vote(x, nik):
    item = execute(f"UPDATE users SET vote = {x} WHERE nik = {nik}")
    item["con"].commit()
    close(item)


def get_status(session):
    if session.get("nik"):
        item = execute(f"SELECT vote FROM users WHERE nik = {session['nik']}")
        res = item["cur"].fetchone()[0]
        close(item)
        if res is None:
            return True
    return False
