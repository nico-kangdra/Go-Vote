from flask import Flask, render_template, flash, request, redirect, session
from services import get_nik, get_count, set_vote, get_status, hash, get_all, insert, delete

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
    return render_template("index.html")


# Login
@app.get("/login")
def getlogin():
    return render_template("login.html")


# Post for Login
@app.post("/login")
def postlogin():
    # Get data from Form
    nama_lengkap = request.form["nama_lengkap"].strip()
    nik = hash(request.form["nik"])
    nama_ibu_kandung = request.form["nama_ibu_kandung"].strip()

    # Check
    if nama_lengkap == "admin" and nama_ibu_kandung == "admin123":
        session.clear()
        session["admin"] = "ADMIN"
        return redirect("/admin")

    # Get nik from SQL in services.py
    res = get_nik(nik)
    if res and res[1] == nama_lengkap and res[2] == nama_ibu_kandung:
        session.clear()
        session["nik"] = nik
        session["nama_lengkap"] = nama_lengkap
        session["nama_ibu_kandung"] = nama_ibu_kandung
        return redirect("/syarat")
    flash("Penduduk tidak ditemukan")
    return redirect("/login")

@app.get("/admin")
def getadmin():
    data = get_all()
    if session.get("admin"):
        return render_template("admin.html", data=data)
    return redirect("/login")

@app.post("/admin")
def postadmin():
    nama_lengkap = request.form["nama_lengkap"].strip()
    nik = hash(request.form["nik"])
    nama_ibu_kandung = request.form["nama_ibu_kandung"].strip()
    insert(nik,nama_lengkap,nama_ibu_kandung)
    return redirect("/admin")

@app.post("/deletes/<string:nik>")
def deletes(nik):
    delete(nik)
    return redirect("/admin")

# Syarat dan Ketentuan
@app.get("/syarat")
def getsyarat():
    # Check session
    if session.get("nik"):
        return redirect("/verif")
    return redirect("/login")


# Face Recognition
@app.get("/verif")
def verif():
    return ""


# Coblos
@app.get("/coblos")
def getcoblos():
    if get_status(session):
        return render_template("coblos.html")
    return redirect("/login")


# Post for Coblos
@app.post("/coblos")
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
    return render_template("preview.html", res=res)


# Logout
@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")


# Run the app when files execute
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
