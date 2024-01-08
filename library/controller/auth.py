from library import app
from library.model import User
from flask import render_template, request, redirect, session


@app.route("/")
def auth_index():
    if session.get("username"):
        return redirect("/home")
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def auth_login():
    if session.get("username"):
        return redirect("home")
    info = request.args.get("info", "")
    if request.method == "POST":
        sql = User(request.form["username"])
        if not sql.login(request.form["password"]):
            info = "error"
        else:
            session["username"] = request.form["username"]
            return redirect("/home")
    return render_template("auth/index.html", info=info)


@app.route("/logout")
def auth_logout():
    session.clear()
    return redirect("/login?info=quit")
