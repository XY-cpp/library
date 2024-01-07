from library import app
from library.model import User
from flask import render_template,session,redirect

@app.route("/home",methods=['GET', 'POST'])
def home_index():
    id = session.get("id")
    if id is None:
        return redirect('/login?info=noid') 
    return render_template('home/index.html')