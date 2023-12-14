from services.db import db_con
from hashlib import sha256


def hash(txt):
    return sha256(txt.encode("utf-8")).hexdigest()


def execute(sql):
    conn = db_con()
    curs = conn.cursor()
    curs.execute(sql)
    return {"con": conn, "cur": curs}


def close(item):
    for x in item.values():
        x.close()


def get_nik(nik):
    item = execute(f"SELECT * FROM users WHERE nik = '{nik}'")
    res = item["cur"].fetchone()
    close(item)
    return res


def get_count():
    item = [
        execute(f"SELECT COUNT(*) FROM users WHERE vote = 1"),
        execute(f"SELECT COUNT(*) FROM users WHERE vote = 2"),
        execute(f"SELECT COUNT(*) FROM users WHERE vote = 3"),
    ]
    res = [
        item[0]["cur"].fetchone()[0],
        item[1]["cur"].fetchone()[0],
        item[2]["cur"].fetchone()[0],
    ]
    res = [res[x] + 1 if res[x] == 0 else x for x in range(len(res))]
    for x in item:
        close(x)
    return res


def set_vote(x, nik):
    item = execute(f"UPDATE users SET vote = {x} WHERE nik = '{nik}'")
    item["con"].commit()
    close(item)


def get_status(session):
    if session.get("nik"):
        item = execute(f"SELECT vote FROM users WHERE nik = '{session['nik']}'")
        res = item["cur"].fetchone()[0]
        close(item)
        if res is None:
            return True
    return False


def get_all():
    item = execute("SELECT nik, nama_lengkap, nama_ibu_kandung FROM users")
    res = item["cur"].fetchall()
    close(item)
    return res


def insert(x, y, z):
    item = execute(
        f"INSERT INTO users (nik, nama_lengkap, nama_ibu_kandung) VALUES ('{x}','{y}','{z}')"
    )
    item["con"].commit()
    close(item)


def delete(x):
    item = execute(f"DELETE FROM users WHERE nik = '{x}'")
    item["con"].commit()
    close(item)
