from library import app
from library.model import *
from flask import render_template, session, redirect, request
from flask_paginate import get_page_parameter, Pagination
import datetime


@app.route("/home")
def home_index():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login?info=noid")
    user = User(user_id)
    borrowed_num = len(Borrow.borrow_id(user_id))
    tle_num = len(Borrow.tle_id(user_id))
    return render_template(
        "home/index.html", name=user.name, borrowed_num=borrowed_num, tle_num=tle_num
    )


@app.route("/home/book")
def home_book():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login?info=noid")
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    pagination = Pagination(
        page=page,
        per_page=per_page,
        total=Icp.total(),
        css_framework="bootstrap4",
        alignment="center",
    )

    start = (page - 1) * per_page + 1
    end = start + per_page
    icp_list = []
    info_list = []
    items_list = []
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

        items = []
        for book_id in Item.get_id_by_isbn(icp.isbn):
            items.append(Item(book_id))
        items_list.append(items)

    return render_template(
        "home/book.html",
        zip=zip,
        icp_list=icp_list,
        info_list=info_list,
        items_list=items_list,
        pagination=pagination,
    )


@app.route("/home/profile")
def home_profile():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login?info=noid")
    user = User(user_id)
    borrow_list = Borrow.get_status(user_id)
    return render_template("home/profile.html", user=user, borrow_list=borrow_list)
