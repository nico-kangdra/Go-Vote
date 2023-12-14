from flask import Flask, render_template, flash, request, redirect, session
from services.services import (
    get_nik,
    get_count,
    set_vote,
    get_status,
    hash,
    get_all,
    insert,
    delete,
)

# Initialize flask app
app = Flask(__name__)
app.secret_key = "COMEGOVOTE"


# Set Session
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = 600


# Homepage
@app.get("/")
def home():
    return render_template("public/index.html")


# Admin Login
@app.get("/login/admin")
def getloginadmin():
    return render_template("/admin/login_admin.html")


# Post for Login
@app.post("/")
def postlogin():
    # Get data from Form
    nama_lengkap = request.form["nama_lengkap"].strip()
    nik = hash(request.form["nik"])
    nama_ibu_kandung = request.form["nama_ibu_kandung"].strip()

    # Get nik from SQL in services.py
    res = get_nik(nik)

    # Check
    if res and res[1] == nama_lengkap and res[2] == nama_ibu_kandung:
        session.clear()
        session["nik"] = nik
        session["nik_ori"] = request.form["nik"]
        session["nama_lengkap"] = nama_lengkap
        session["nama_ibu_kandung"] = nama_ibu_kandung
        return redirect("/profile")
    flash("Penduduk tidak ditemukan")
    return redirect("/")


# Post for Login
@app.post("/login/admin")
def postloginadmin():
    # Get data from Form
    id = request.form["id"]
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    # Check
    res = get_nik(id)
    if res and res[1] == username and res[2] == password:
        session.clear()
        session["admin"] = "ADMIN"
        return redirect("/admin")


@app.get("/admin")
def getadmin():
    data = get_all()
    if session.get("admin"):
        return render_template("admin/admin.html", data=data)
    return redirect("/login/admin")


@app.post("/admin")
def postadmin():
    nama_lengkap = request.form["nama_lengkap"].strip()
    nik = hash(request.form["nik"])
    nama_ibu_kandung = request.form["nama_ibu_kandung"].strip()
    insert(nik, nama_lengkap, nama_ibu_kandung)
    return redirect("/admin")


@app.post("/deletes/<string:nik>")
def deletes(nik):
    delete(nik)
    return redirect("/admin")


# Syarat dan Ketentuan
@app.get("/profile")
def getProfile():
    # Check session
    if session.get("nik"):
        return render_template("/user/profile.html")
    return redirect("/")


# Syarat dan Ketentuan
@app.get("/syarat")
def getsyarat():
    # Check session
    if session.get("nik"):
        return render_template("/user/syarat.html")
    return redirect("/")


# Face Recognition
@app.get("/verify")
def verif():
    if session.get("nik"):
        return render_template("/user/verify.html")
    return redirect("/")


# Coblos
@app.get("/vote")
def getcoblos():
    if get_status(session):
        return render_template("/user/vote.html")
    return redirect("/")


# Post for Coblos
@app.post("/vote")
def postcoblos():
    if session.get("nik"):
        vote = request.form["vote"]
        set_vote(int(vote), session["nik"])
        return redirect("/preview")
    return redirect("/login")


# Preview
@app.get("/preview")
def preview():
    res = get_count()
    res = [round(x / sum(res) * 100, 2) for x in res]
    return render_template("/user/preview.html", res=res)


# Logout
@app.get("/logout")
def logout():
    session.clear()
    return redirect("/")


# Run the app when files execute
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
