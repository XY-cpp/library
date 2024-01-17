from library import app
from library.model import User
from flask import render_template, request, redirect, session


@app.route("/")
def auth_index():
    if session.get("user_id"):
        user = User(session.get("user_id"))
        if user.admin:
            return redirect("/admin")
        else:
            return redirect("/home")
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def auth_login():
    if session.get("user_id"):
        return redirect("/")
    info = request.args.get("info", "")
    if request.method == "POST":
        user_id = User.login(request.form["username"], request.form["password"])
        if user_id:
            session["user_id"] = user_id
            return redirect("/")
        else:
            info = "error"
    return render_template("auth/index.html", info=info)


@app.route("/logout")
def auth_logout():
    session.clear()
    return redirect("/login?info=quit")
