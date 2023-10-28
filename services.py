from db import db_con


def execute(sql):
    conn = db_con()
    curs = conn.cursor()
    curs.execute(sql)
    return [conn, curs]


def close(item):
    for x in item:
        x.close()


def get_nik(nik):
    item = execute(f"SELECT * FROM users WHERE nik = {nik}")
    res = item[1].fetchone()
    close(item)
    return res


def get_count():
    item1 = execute(f"SELECT COUNT(*) FROM users WHERE vote = 1")
    item2 = execute(f"SELECT COUNT(*) FROM users WHERE vote = 2")
    item3 = execute(f"SELECT COUNT(*) FROM users WHERE vote = 3")
    res = [item1[1].fetchone()[0], item2[1].fetchone()[0], item3[1].fetchone()[0]]
    close(item1)
    close(item2)
    close(item3)
    return res


def set_vote(x, nik):
    item = execute(f"UPDATE users SET vote = {x} WHERE nik = {nik}")
    item[0].commit()
    close(item)


def get_status(session):
    if session.get("nik"):
        item = execute(f"SELECT vote FROM users WHERE nik = {session['nik']}")
        res = item[1].fetchone()[0]
        close(item)
        if res is None:
            return True
    return False
