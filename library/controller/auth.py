from library import app
from library.model import User
from flask import render_template, request, redirect, session


@app.route("/")
def auth_index():
    print(session.get("user_id"))
    if session.get("user_id"):
        return redirect("/home")
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def auth_login():
    if session.get("user_id"):
        return redirect("home")
    info = request.args.get("info", "")
    if request.method == "POST":
        user_id = User.login(request.form["username"], request.form["password"])
        if user_id :
            session["user_id"] = user_id
            return redirect("/home")
        else:
            info = "error"
    return render_template("auth/index.html", info=info)


@app.route("/logout")
def auth_logout():
    session.clear()
    return redirect("/login?info=quit")
