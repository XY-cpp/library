from library import app
from library.db import Sql
from flask import render_template, request

username = "username"
password = "password"

@app.route("/",methods=['GET', 'POST'])
def login():
    error = False
    if request.method == 'POST':
        sql = Sql()
        username = request.form['username']
        password = request.form['password']
        result = sql.get_one("select * from user where id = %s and pwd = %s",(username,password))
        if result == None:
            error = True 
        else:
            return "success"
    return render_template('auth/login.html', error=error)