from library import app
from library.model import User
from flask import render_template, request, redirect 


@app.route("/", methods=["GET", "POST"])
def auth_login():
    error = False
    if request.method == "POST":
        sql = User(request.form["username"])
        if not sql.login(request.form["password"]):
            error = True
        else:
            return redirect("/home")
    return render_template("auth/login.html", error=error)