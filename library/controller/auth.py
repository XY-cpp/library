from library import app
from library.model import User
from flask import render_template, request, redirect, session

@app.route("/")
def auth_index():
    if session.get("id"):
        return redirect("/home")
    else: return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def auth_login():
    info = request.args.get('info','')
    if request.method == "POST":
        sql = User(request.form["username"])
        if not sql.login(request.form["password"]):
            info = "error"
        else:
            session["id"]=request.form["username"]
            return redirect("/home")
    return render_template("auth/login.html", info=info)