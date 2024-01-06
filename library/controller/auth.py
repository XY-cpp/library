from library import app
from library.model import Model
from flask import render_template, request

username = "username"
password = "password"

@app.route("/",methods=['GET', 'POST'])
def login():
    error = False
    if request.method == 'POST':
        sql = Model()
        username = request.form['username']
        password = request.form['password']
        # print(sql.get_all("show tables"))
        sql.connect()
        result = sql.get_one("select * from user where id = %s and pwd = %s",(username,password))
        # print(result)
        if result == None:
            error = True 
        else:
            return "success"
    return render_template('auth/login.html', error=error)