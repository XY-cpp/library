from library import app
from library.model import User, Icp, Item
from flask import render_template, session, redirect, request
from flask_paginate import get_page_parameter, Pagination


@app.route("/admin")
def admin():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login?info=noid")
    user = User(user_id)
    return render_template("admin/index.html", name=user.name)


@app.route("/admin/book", methods=["POST", "GET"])
def admin_book():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login?info=noid")

    if request.method == "POST":
        mp = request.form.to_dict()
        Icp.update(mp)

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
    end = min(start + per_page, pagination.total + 1)
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
            ("id", icp.id),
        ]
        info_list.append(info)

        items = []
        for book_id in Item.get_id_by_isbn(icp.isbn):
            items.append(Item(book_id))
        items_list.append(items)

    return render_template(
        "admin/book.html",
        zip=zip,
        icp_list=icp_list,
        info_list=info_list,
        items_list=items_list,
        pagination=pagination,
    )


@app.route("/admin/profile")
def admin_profile():
    username = session.get("user_id")
    if username is None:
        return redirect("/login?info=noid")
    user = User(username)
    return render_template("admin/profile.html", user=user)



@app.route("/admin/borrow", methods=["POST","GET"])
def admin_borrow():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login?info=noid")
    
    if request.method == "POST":
        mp = request.form.to_dict()
        Item.update(mp)


    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    pagination = Pagination(
        page=page,
        per_page=per_page,
        total=Item.total_items(),
        css_framework="bootstrap4",
        alignment="center",
    )

    start = (page - 1) * per_page + 1
    end = min(start + per_page, pagination.total + 1)
    icp_list = []
    info_list = []
    items_list = []
    
    for id in range(start, end):

        item = Item(id)

        #items_list.append(item)
        #info_list.append(item)
        #icp_list.append(item)
        
        name = Item.get_name_by_isbn(item.isbn)[0]
        #("书名", item.get_name_by_isbn(item.isbn)[0])

        info = [
                ("书名", name),
                ("ISBN", item.isbn),
                ("地点", item.location),
                ("id", item.id),
                ("状态", item.status),
        ]

        info_list.append(info)
        items_list.append(item)
        """
        items = []
        for book_id in Item.get_id_by_isbn(icp.isbn):
            items.append(Item(book_id))
        items_list.append(items)
        """


    return render_template(
        "admin/borrow.html",
        zip=zip,
        icp_list=icp_list,
        info_list=info_list,
        items_list=items_list,
        pagination=pagination,
    )


@app.route("/admin/addbook", methods=["POST","GET"])
def admin_addbook():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login?info=noid")
    
    if request.method == "POST":
        mp = request.form.to_dict()
        number = int(mp['数目'])
        book = Icp.find_by_isbn(mp['ISBN'])
        mp['经办人'] = user_id
        if book is None:
            Icp.insert(mp)
        

        book = Icp.find_by_isbn(mp['ISBN'])
        Icp.update_number(number, book[4])

        for i in range(0,number):
            Item.add(mp['ISBN'],mp['地点'])

    username = session.get("user_id")
    if username is None:
        return redirect("/login?info=noid")
    user = User(username)
    return render_template("admin/addbook.html", user=user)