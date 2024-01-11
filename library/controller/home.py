from library import app
from library.model import User, Icp, BookStatus
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
    icp_list = []
    info_list = []
    for id in range(start, end):
        icp = Icp(id)
        icp_list.append(icp)
        info = [
            ("书名", icp.name),
            ("作者", icp.author),
            ("出版商", icp.press),
            ("ISBN", icp.isbn),
            ("出版日期", icp.press_time),
            ("经办人", icp.manger),
        ]
        info_list.append(info)
    return render_template(
        "home/book.html",
        zip=zip,
        icp_list=icp_list,
        info_list=info_list,
        pagination=pagination,
    )
