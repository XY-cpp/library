from library import app
from library.model import User, Icp
from flask import render_template, session, redirect, request
from flask_paginate import get_page_parameter, Pagination


@app.route("/home", methods=["GET", "POST"])
def home_index():
    username = session.get("username")
    if username is None:
        return redirect("/login?info=noid")
    user = User(username)
    return render_template("home/index.html", name=user.name())


@app.route("/home/book")
def home_book():
    username = session.get("username")
    if username is None:
        return redirect("/login?info=noid")
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    pagination = Pagination(
        page=page,
        per_page=per_page,
        total=Icp.total_books(),
        css_framework="bootstrap4",
        alignment="center",
    )

    start = (page - 1) * per_page + 1
    end = start + per_page
    books = [Icp(i) for i in range(start, end)]

    return render_template("home/book.html", books=books, pagination=pagination)
