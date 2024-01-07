from library import app
from library.model import User
from flask import render_template, request

@app.route("/",methods=['GET', 'POST'])
def login():
    error = False
    if request.method == 'POST':
        sql = User(request.form['username'])
        if not sql.login(request.form['password']):
            error = True 
        else:
            return "success"
    return render_template('auth/login.html', error=error)