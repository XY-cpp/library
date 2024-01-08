from library import app
from library.model import User
from flask import render_template, session, redirect


@app.route("/home", methods=["GET", "POST"])
def home_index():
    username = session.get("username")
    if username is None:
        return redirect("/login?info=noid")
    user = User(username)
    return render_template("home/index.html",name=user.name())